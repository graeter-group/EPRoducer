
==================
spectrum_from_gval
==================

.. container:: bash-script-title

   :ref:`[script] <script-spectrum_from_gval>` **eproducer/spectrum_from_gval.sh**

.. container:: bash-script-doc

   .. line-block::

      Creates the EPR absorption spectrum from a set of g-values using EasySpin.

        -a  <float> modulation amplitude in mT.
        -e  <file.dat> experimental field vs absorption file. Its first column is
            used to define the field range of the predicted spectrum.
        -g  <g-values> g-values used to predict the spectrum, e.g. '[ 2.0 2.0 2.0 ]'.
        -A  <A-values> hyperfine coupling values (HSC) in mT, one row per nucleus
            group, e.g. '[ 1.40 1.55 1.94 ]' or, for two nucleus groups,
            '[ 1.40 1.55 1.94 ; 2.94 2.94 2.94 ]'. Values are converted from mT to
            MHz (EasySpin's Sys.A units) using the isotropic average of the
            g-values given with -g. If not given, no hyperfine correction is
            applied.
        -N  <Sys.Nucs> comma-separated nucleus identifiers, one per row of -A, e.g.
            '1H,1H,1H' for three equivalent 1H nuclei sharing the same A-row.
            Equivalent nuclei must be listed explicitly (repeated), Sys.n is not
            used. Defaults to as many '1H' as rows in -A.
        -o  <output.dat> dat output file where the field vs spectrum is saved. If it
            is not given, it is generated from the g-values.
        -l  <lwpp=1> linewidth.
        -m  <float=179.813> experimental value of the microwave frequency. The
            default value corresponds to G-band experiments.
        -M  <matlab='matlab'> command used to call matlab.
        -n  <int=401> number of data points used to predict the absorption spectrum.
        -t  <int=0> type of spectrum. 0 for absorption, 1 for first derivative, 2 for
            second derivative.

        -v  verbose.
        -h  prints this message.
