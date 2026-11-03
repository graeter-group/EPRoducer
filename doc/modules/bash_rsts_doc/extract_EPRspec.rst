
===============
extract_EPRspec
===============

.. container:: bash-script-title

   :ref:`[script] <script-extract_EPRspec>` **eproducer/extract_EPRspec.sh**

.. container:: bash-script-doc

   .. line-block::

      Extract the EPR absorption spectrum from an orca output file.

        -a  <float> modulation amplitude in mT.
        -d  <disturb g-tensor='[ 0 0 0 ]'> disturbance to the g-tensor. It can vary
            because of thermal effects or interactions not considered in the QM
            calculations (like solvent).
        -e  <file.dat> experimental field vs absorption file.
        -f  Use this flag to take into account hyperfine corrections. This uses a lot
            of RAM memory. Be sure that you have enough memory or that you filtered
            the nuclei to compute hyperfine correction.
        -O  <file.out='epr_info.out'> orca output file with computed EPR quantities.
        -o  <output.dat='spectrum_wo_hyFiCorr.dat'> dat output file where you want to
            save the field vs spectrum.
        -l  <lwpp=1> linewidth
        -s  <gStrain> g-strain (EasySpin's Sys.gStrain), i.e. FWHM of the
            distribution of each g-value, in the same order as the g-values read from
            the orca output (the same order used by -d), which is increasing. It
            broadens each principal direction separately, e.g. '[0,0,0.0015]' smooths
            only the low-field edge (largest g-value). If not given, no g-strain is
            applied.
        -m  <float=179.813> experimental value of the microwave frequency. The
            default value corresponds to G-band experiments.
        -n  <int=401> number of data points used to predict the absorption spectrum.
        -t  <int=0> type of spectrum. 0 for absorption, 1 for first derivative, 2 for
            second derivative.

        -v  verbose.
        -h  prints this message.
