"""
Spectral fitting of computed EPR spectra against experimental data using
non-negative least squares.
"""

import numpy as np
from scipy.optimize import nnls
from eprtools.miscellaneous import output_terminal
from PlottingTool import StandardPlotter
from scipy.io import loadmat
from scipy.stats import pearsonr


class TheoMatchExpe:
    """
    Collects the computed data and tries to fit it to the experiment spectrum

    Parameters
    ==========
    files: list
        paths to the .dat files (field vs intensity) of the computed spectra
        of the candidates.
    experiment_file: str. Default=None
        .dat field vs intensity of the experiment. If None, the first file of
        files is used as experiment.
    **kwargs:
        passed to TheoMatchExpe.fit_shifting, e.g. fieldrange or
        shifting_width.

    Note
    ====
    The computed spectra are interpolated onto the field values of the
    experiment, and the experimental intensities are normalized to a maximum
    of 1.
    """
    def __init__(self,
                 files,
                 experiment_file=None,
                 **kwargs):
        """
        Loads and normalizes the experimental spectrum and fits the computed
        spectra to it (see TheoMatchExpe.fit_shifting). See the class docstring
        for the parameters.
        """
        self.shifting_width = 0
        self.shift = 0
        self.fieldrange = None
        if experiment_file is None:
            self.fieldexp, self.intensexp = np.loadtxt(files[0], unpack=True)
            self.intensexp = self.intensexp / max(self.intensexp)
        else:
            self.fieldexp, self.intensexp = np.loadtxt(experiment_file,
                                                       unpack=True)
            self.intensexp = self.intensexp / max(self.intensexp)

        self.files = np.array(files)
        self.files_bck = self.files.copy()

        theoretical = self.fit_shifting(**kwargs)
        self.coeffs, self.intensities, \
            self.intensfit, self.error, self.corr = theoretical

        self.proportions()


    def fit_theoretical(self, files=None, fieldexp=None, fieldrange=None):
        """
        Fits the experimental spectrum with a non-negative linear combination of
        the computed spectra (non-negative least squares).

        Parameters
        ==========
        files: list. Default=None
            paths to the .dat files of the computed spectra. If None,
            TheoMatchExpe.files is used.
        fieldexp: numpy.array. Default=None
            field values where the computed spectra are interpolated. If None,
            TheoMatchExpe.fieldexp is used.
        fieldrange: list. Default=None
            [min, max] field range to fit. The experimental intensities outside
            this range (shifted by TheoMatchExpe.shift) are set to zero before
            fitting. If None, the whole range is used.

        Return
        ======
        (tuple) coeffs [n_files x 1] of the linear combination, intensities
        [n_files x n_points] interpolated computed spectra, intensfit [n_points]
        fitted spectrum, error (residual of the fit) and corr (Pearson
        correlation between the fitted spectrum and the experiment).
        """
        if files is None:
            files = self.files
        if fieldexp is None:
            fieldexp=self.fieldexp
        if fieldrange is None:
            # takes all the range
            self.condition = np.logical_not(fieldexp == fieldexp)
        else:
            self.condition = np.logical_or(fieldexp < fieldrange[0] + self.shift,
                                           fieldexp > fieldrange[1] + self.shift)
        tmp_inten = self.intensexp.copy()
        tmp_inten[self.condition] = 0

        intensities = []
        for file in files:
            try:
                field_p = np.loadtxt(file, usecols=0)
            except FileNotFoundError:
                field_p = None
                intensities.append(None)
                continue
            intensity_p = np.loadtxt(file, usecols=1)
            intensity = np.interp(fieldexp, field_p, intensity_p)
            intensities.append(intensity)
        intensities = np.array(intensities)

        # Interpolate and find coeffs
        A = np.column_stack([bf for bf in intensities])
        coeffs, error = nnls(A, tmp_inten)
        coeffs = coeffs.reshape(len(intensities), 1)
        intensfit = np.sum(coeffs * intensities, axis=0)
        corr = pearsonr(intensfit,
                        self.intensexp)[0]

        return coeffs, intensities, intensfit, error, corr

    def fit_shifting(self, files=None, shifting_width=None, shift_step=0.2,
                     **kwargs):
        """
        Shifts the experimental field within [-shifting_width, shifting_width]
        and keeps the shift whose fit (see TheoMatchExpe.fit_theoretical) has the
        smallest residual. The results are stored in the attributes coeffs,
        intensities, intensfit, error, corr and shift.

        Parameters
        ==========
        files: list. Default=None
            paths to the .dat files of the computed spectra. If None,
            TheoMatchExpe.files is used.
        shifting_width: float. Default=None
            maximum shift of the field in both directions. If None, the last
            value given is used (0 at the beginning, i.e. no shifting).
        shift_step: float. Default=0.2
            step between the tested shifts.
        **kwargs:
            fieldrange: list. [min, max] field range to fit. If not given, the
            last value given is used. None (the initial value) means the
            whole range of the experiment.

        Return
        ======
        (tuple) coeffs, intensities, intensfit, error and corr of the best shift.
        See TheoMatchExpe.fit_theoretical.
        """
        if files is None:
            files = self.files
        min_error = float('inf')
        if shifting_width is not None:
            self.shifting_width = shifting_width
        if self.shifting_width == 0:
            shift_interval = [0]
        else:
            shift_interval = np.arange(-self.shifting_width,
                                       self.shifting_width + shift_step,
                                       shift_step)
        # stored like shifting_width, so the refits done while cleaning the
        # candidates keep the same range
        if 'fieldrange' in kwargs.keys():
            self.fieldrange = kwargs.pop('fieldrange')
        if self.fieldrange is None:
            interval = np.array([min(self.fieldexp),
                                 max(self.fieldexp)])
        else:
            interval = np.array(self.fieldrange)

        for shift in shift_interval:
            exp_intensity = self.fieldexp + shift
            fitting = self.fit_theoretical(files, exp_intensity,
                                           fieldrange= interval + shift,
                                           **kwargs)
            coeffs, intensities, intensfit, error, corr = fitting
            if error <= min_error:
                min_error = error
                self.error = error
                self.intensities = intensities
                self.coeffs = coeffs
                self.intensfit = intensfit
                self.shift = shift
                self.corr = corr
        self.proportions()

        return self.coeffs, self.intensities, self.intensfit, min_error, \
            self.corr


    def proportions(self, print_analysis=False):
        """
        Computes the percentage of each one of the candidates that fit better
        the experimental spectrum.

        Parameters
        ==========
        print_analysis: Bool. Default=False
            True to print the percentage of each one of the candidates.

        Return
        ======
        (np.array) percentages.
        """
        total = np.sum(self.coeffs)
        self.percentages = 100 * self.coeffs.flatten() / total
        if print_analysis:
            for i in np.argsort(-self.percentages):
                print(self.files[i], " (%): ", self.percentages[i])

        return self.percentages

    def gradual_cleaning(self, threshold=1, steps=0.1, **kwargs):
        """
        Removes gradually the candidates that do not weight much in the fitting
        up to having all the candidates with a minimum percentage in the fitting.
        It starts again from all the candidates given initially.

        Parameters
        ==========
        threshold: float. Default=1
            minimum percentage per candidate to be considered into the fitting.
        steps: float. Default=0.1
            size of the steps in the filtering.
        **kwargs:
            passed to TheoMatchExpe.fit_shifting, e.g. shifting_width.

        Return
        ======
        (np.array) new set of intensities.
        """
        self.files = self.files_bck
        self.fit_shifting(self.files, **kwargs)
        for intermedia in np.arange(steps, threshold, steps):
            output = self.clean_candidates(threshold=intermedia, **kwargs)
        output = self.clean_candidates(threshold=threshold, **kwargs)

        return output

    def clean_candidates(self, threshold=1, **kwargs):
        """
        Removes the candidates that are expected to be less than certain
        percentage. It means, TheoMatchExpe.intensities and TheoMatchExpe.files
        might be reduced. The fit is repeated until all the remaining
        candidates reach the threshold.

        Parameters
        ==========
        threshold: float. Default=1
            minimum percentage that a candidate should have to be considered.
        **kwargs:
            passed to TheoMatchExpe.fit_shifting, e.g. shifting_width.

        Return
        ======
        (np.array) new set of intensities.
        """
        self.proportions()
        condition = self.percentages >= threshold
        if condition.all():
            return self.intensities

        self.files = self.files[condition]
        self.fit_shifting(self.files, **kwargs)
        return self.clean_candidates(threshold=threshold)


# The subsequent functions were not addapted to shifting.
def fit_experiment(experiment_file='../experiments/field_vs_spectrum.dat',
                   basis_pattern='spectrum_wo_hyFiCorr.dat'):
    """
    Collects the computed data and tries to fit it to the experiment spectrum

    Parameters
    ==========
    experiment_file: str. Default='../experiments/field_vs_spectrum.dat'
        .dat field vs intensity of the experiment.
    basis_pattern: str. Default='spectrum_wo_hyFiCorr.dat'
        pattern of the .dat files containing the spectrum of the computed spectrum.

    Return
    ======
    (tuple) fieldexp and intensexp of the experiment, field of the computed
    spectra and best_fit_intensity [n_files x n_points], i.e. each computed
    spectrum multiplied by its coefficient in the fit.

    Note
    ====
    This script assumes that the basis files has a common pattern and they are all
    in subdirectories of '../'. It also assumes that all the values of the
    computed intensities are defined for the same values of the field.
    """
    fieldexp, intensexp = np.loadtxt(experiment_file, unpack=True)
    files = output_terminal(f"find ../ -name '{basis_pattern}' | sort",
                            print_output=False)
    files = files.split('\n')[:-1]

    field = np.loadtxt(files[0], usecols=0)
    intensities = []
    for file in files:
        intensity = np.loadtxt(file, usecols=1)
        intensities.append(intensity)
    intensities = np.array(intensities)

    # Interpolate and find coeffs
    A = np.column_stack([np.interp(fieldexp, field, bf) for bf in intensities])
    coeffs, _ = nnls(A, intensexp)

    best_fit_intensity = coeffs.reshape(len(intensities), 1) * intensities

    return fieldexp, intensexp, field, best_fit_intensity


# add2executable
def create_fit_file(output,
                    experiment_file='../experiments/field_vs_spectrum.dat',
                    basis_pattern='spectrum_wo_hyFiCorr.dat',
                    basis_location='../'):
    """
    Creates a .dat file with field vs intensity of the best fit to an
    experiment with some given calculated spectrums.

    Parameters
    ==========
    output: str
        name of the .dat file where you want to store the output.
    experiment_file: str. Default='../experiments/field_vs_spectrum.dat'
        .dat field vs intensity of the experiment.
    basis_pattern: str. Default='spectrum_wo_hyFiCorr.dat'
        pattern of the .dat files containing the spectrum of the computed spectrum.
    basis_location: str. Default='../'
        location where to search for the files with the basis_pattern.

    Return
    ======
    (None) it does not return anything but creates the .dat file with the fit.

    Note
    ====
    The basis files are searched recursively in basis_location. They are
    interpolated onto the field of the experiment (see TheoMatchExpe).
    """
    files = output_terminal(f"find {basis_location} -name '{basis_pattern}'", print_output=False)
    files = files.split('\n')[:-1]
    tme = TheoMatchExpe(files, experiment_file)
    field = tme.fieldexp
    inten = tme.intensfit

    with open(output, 'w') as outfile:
        outfile.write('# field intensity\n')
        for f, i in zip(field, inten):
            outfile.write(f'{f} \t {i} \n')


# add2executable
def spect_w_experiment(experiment, theory, output):
    """
    Fits the peak of the theoretical spectrum into the experimental value at
    that value of the field and saves a plot of both spectra.

    Parameters
    ==========
    experiment: str
        path to the .dat file containing the experimental field and the
        intensity.
    theory: str
        path to the .dat file containing the theoretical field and the
        intensity of the given candidate.
    output: str
        name of the png file where the output is stored.

    Return
    ======
    (None) it saves the plot of both spectra in output.
    """
    fieldexp, intensexp = np.loadtxt(experiment, unpack=True)
    field, intens = np.loadtxt(theory, unpack=True)

    maxintensity_index = intens.argmax()
    target_field_val = field[maxintensity_index]
    closest_exp_index = np.abs(fieldexp - target_field_val).argmin()
    experiment_val =intensexp[closest_exp_index]
    intens = intens * experiment_val / intens[maxintensity_index]

    sp = StandardPlotter(ax_pref={'xlabel': 'Field [T]',
                                  'ylabel': 'Intensity [a.u]'})
    sp.plot_data(field, intens, pstyle='-', data_label='Theory')
    sp.plot_data(fieldexp, intensexp, pstyle='-', color_plot='black', data_label='Experiment')
    sp.spaces[0].set_axis(borders=[[0.15, 0.15], [0.98, 0.98]])
    sp.axis_setter(legend=True)
    sp.save(output)


# add2executable
def best_fit(experiment, output, fieldrange, *argv):
    """
    Fits an experimental spectrum with the computed spectra of several
    candidates, keeps the candidates that contribute at least 5 % to the fit,
    prints their percentages and saves a plot of the fit.

    Parameters
    ==========
    experiment: str
        path to the .dat file containing the experimental field and the
        intensity.
    output: str
        name of the png file where the plot is stored.
    fieldrange: str
        [min, max] field range to fit in python list format, e.g.
        '[640, 650]'. Use '' to fit the whole range. The range is marked with
        dotted lines in the plot.
    *argv: str
        paths to the .dat files containing the computed spectra of the
        candidates.

    Return
    ======
    (None) it prints the percentage of each candidate and the shift of the
    field, and saves the plot in output.

    Note
    ====
    The experimental field is shifted up to 10 units in both directions (in
    steps of 0.2) to find the best fit. See TheoMatchExpe.fit_shifting.
    """
    if fieldrange == '':
        fieldrange = None
    else:
        fieldrange = eval(fieldrange)
    files = list(argv)
    tme = TheoMatchExpe(files,
                        experiment_file=experiment,
                        fieldrange=fieldrange,
                        shifting_width=10)
    tme.gradual_cleaning(threshold=5)
    tme.proportions(print_analysis=True)

    sp = StandardPlotter(ax_pref={'xlabel': 'Field [T]',
                                  'ylabel': 'Intensity [a.u]'},
                     plot_pref={'pstyle': '-'})
    sp.plot_data(tme.fieldexp + tme.shift, tme.intensexp, pstyle='-', color_plot='black', data_label='Experiment')
    sp.plot_data(tme.fieldexp, tme.intensfit, pstyle='-', data_label='Fit')
    sp.plot_data(tme.fieldexp, tme.coeffs * tme.intensities, pstyle='--');
    if fieldrange is not None:
        sp.plot_data([fieldrange[0], fieldrange[0]], [0, 1], pstyle=':', color_plot='gray');
        sp.plot_data([fieldrange[1], fieldrange[1]], [0, 1], pstyle=':', color_plot='gray');
    sp.spaces[0].set_axis(borders=[[0.15, 0.15], [0.98, 0.98]])
    sp.axis_setter(legend=True)
    sp.save(output)
    print('shifting of: ', tme.shift)


# add2executable
def mat2dat(file_field: str, file_spectrum: str, output: str):
    """
    Converts an experimental spectrum stored in MATLAB .mat files into a .dat
    file with two columns: field and spectrum.

    Parameters
    ==========
    file_field: str
        .mat file containing the field in a variable called 'fieldexp'.
    file_spectrum: str
        .mat file containing the intensities in a variable called 'specexp'.
    output: str
        name of the .dat file where the field vs spectrum is saved.

    Return
    ======
    (None) it creates the .dat file.
    """
    try:
        data = loadmat(file_field)
        field = data['fieldexp'].flatten()
        data = loadmat(file_spectrum)
        spectrum = data['specexp'].flatten()
    except:
        raise ValueError("error reading matlab data, be sure that the name of" +
                         "the data is fieldexp and specexp")

    rows = np.append([field], [spectrum], axis=0).T
    with open(output, 'w') as fil:
        fil.write("# field spectrum\n")
        for row in rows:
            fil.write(f"{row[0]} \t {row[1]}\n")
