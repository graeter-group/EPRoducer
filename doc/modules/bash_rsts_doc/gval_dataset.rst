
============
gval_dataset
============

.. container:: bash-script-title

   :ref:`[script] <script-gval_dataset>` **eproducer/gval_dataset.sh**

.. container:: bash-script-doc

   .. line-block::

      This script select n molecules, out of N molecules that minimizes one of the
      entries in the npz dile. Then, it goes through the selected molecules,
      optimizes them and then computes the g-values and A-matrices (HFC) of the atoms
      in the second degree neighborhood of the relevant atoms defined in the npz
      files, which are marked as 'heavy_atom_missing_idxs' and
      'atom_chargerelevant_idx'.

        -e  <entry='energy_MACE'> entry of the npz file from where the Nmin are
            selected.
        -E  <ending='_epr.out'> ending of the of the files that are excluded in the
            selection of random radicals to compute. In the default case, it excludes
            the radicals that already have an optimization, for example, it excludes
            3 if <file>_003_epr.out already exists.
        -f  <file> file with list of npz files to analyze.
        -j  <job_options='--nice'> joboptions. avoid to add '-n' in this string; that
            variable enters as  the flag -p in of this script.
        -n  <n=1> number of radicals to be selected from each npz file.
        -N  <N=3> number of radicals in the subset that minimizes the entry
            parameter.
        -o  <other_flags=''> extra flags passed through to 'eproducer gval_workflow'.
        -p  <processors=8> number of processors requested for each submitted job.
        -r  Use this flag to RESTART the optimization; it is forwarded as the -R
            flag to 'eproducer gval_workflow'.

        -v  verbose.
        -h  prints this message.
