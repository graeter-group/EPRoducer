
=============
gval_workflow
=============

.. container:: bash-script-title

   :ref:`[script] <script-gval_workflow>` **eproducer/gval_workflow.sh**

.. container:: bash-script-doc

   .. line-block::

      This tool runs all the necessary steps to get the g-values. It works with some
      flags:

        -b  Use this flag to AVOID computation of frequencies.
        -c  <charge=0> charge of the system.
        -d  <directory='.'> directory containing at least model.xyz
        -e  Use this flag to AVOID computation of gvalues. Flags -f and -g are
            unuseful when this flag is activated.
        -f  <hyperfine=''> indexes of atoms to be included in hyperfine corrections.
            If the argument of this flag starts with g, the guess util
            'eproducer iHFC_fromxyz' is used to find the H, O, and N atoms around the
            indexes atoms with the indexes given in the arguments. If you use the
            guess util, be sure to add the depth of the neighborhood with the letter
            d. E.g. 'g4,5d3' finds the relevant atoms in the 3-depth-neigborhood of
            the atoms 4 and 5.
        -g  <reference_mol=''> guess the location of the radical assuming an
            abstraction process. Give the path of the file of the molecule before
            the abstraction.
        -m  <multiplicity=2> multiplicity of the system.
        -n  <prior_name='model'> name of the input and output files. The script needs
            at least a file called prior_name.xyz in the running directory (-d). Then,
            it creates files called prior_name_opt., prior_name_epr., etc.
        -o  Use this flag to AVOID the optimization step. <prior_name>_opt.xyz must
            exist, then.
        -p  <processors=16> number of processors used in the orca calculations.
        -P  Use this flag to ENABLE preemption. When the job is preempted (or hits
            its time limit) it resubmits itself with the same allocation (processors,
            nice value, job name and partition) using the -R restart option, so a
            higher priority job can run first.
        -r  <reference_mol=''> guess the location of the radical assuming an
            abstraction process. Give the path of the file of the molecule before
            the abstraction.
        -R  Use this flag to RESTART the optimization. It uses the file
            <prior_name>_opt.xyz as the input geometry for the optimization.
        -s  Use this flag to delete orca files like gbw...
        -x  <xc='B3LYP EPR-II'> functional and basis set for the g-value calculation.
            The default is B3LYP EPR-II, which is a good choice for g-values.

        -h   prints this message.
        -v   verbose.
