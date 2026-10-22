
============
gval_postpro
============

.. container:: bash-script-title

   :ref:`[script] <script-gval_postpro>` **eproducer/gval_postpro.sh**

.. container:: bash-script-doc

   .. line-block::

      Create all the files after complete the computation of the gvalues with Orca.

        -c  <molecule candidate> Name of the radical candidate. It is assumed that
            the files related with this candidate are in a directory with the same
            name.
        -E  <experimental values> guess of the gvalues obtained experimentally in
            python list format, f.e. '[2.0062, 2.0055, 2.0022]'
        -e  <experiment1.dat,exp2.dat,...> experimental field vs absorption files in
            which this candidate can play a role. Relative paths are taken from each
            candidate directory, e.g. '../../experiments/exp.dat'.
        -o  <output.dat='spectrum_wo_hyFiCorr.dat'> dat output file where you want to
            save the field vs spectrum. Several outputs can be given separated by
            commas, f.e. 'out1.dat,out2.dat'. In that case, the number of outputs must
            match the number of experiments (-e) and they are compared pairwise.
        -O  <orca_output='epr_info.out'> name of the orca output file containing the
            gvalues.

        -v  verbose.
        -h  prints this message.

      This code should produce:

       - A render of each model called opt.png
       - The computed spectrum obtained by easyspin in a file called spectrum_wo_hyFiCorr.dat
       - A plot of the gvalues of all the candidates called gvalues.png
       - A table of the gvalues in gvalues_table.md
       - A file called vmd_image.md in each one of the directories of the candidates.

      This code should be executed in the folder containing the candidate, not in the
      candidate directly.
