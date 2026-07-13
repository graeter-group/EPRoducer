Command-line interface
======================

``eprtools`` exposes Python functions and shell scripts through a unified CLI.
The general usage is::

    eprtools <command> [args...]

Pass ``-h`` as the first argument to any command for its docstring::

    eprtools <command> -h

Python commands
---------------

g-value extraction and post-processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: none

    eprtools extract_gvals        <orca_out>
    eprtools add_gval2npz         <path>
    eprtools extract_system_info  <sys_path> <exp_values> [orca_output]
    eprtools create_table_per_system  <experiment> <systems> [orca_file]
    eprtools create_table_per_method  <data> <experiment> <methods>
    eprtools compute_bde          <reactants> <products>

Spectral fitting
~~~~~~~~~~~~~~~~

.. code-block:: none

    eprtools best_fit             <experiment> <output> <fieldrange> [files...]
    eprtools spect_w_experiment   <experiment> <theory> <output>
    eprtools create_fit_file      <output> [experiment_file] [basis_pattern] [basis_location]
    eprtools mat2dat              <file_field> <file_spectrum> <output>

Structure utilities
~~~~~~~~~~~~~~~~~~~

.. code-block:: none

    eprtools ext_xyz_from_npz     <npz_file> [selection] [create_xyz_files]
    eprtools nrand_rad            <npz_file> [n] [Nmin] [entry] [exclude]
    eprtools heavya_idx_from_ref  <ref_mol_xyz> <rad_mol_xyz> <index> [engine]
    eprtools rad_loc              <ref_mol_xyz> <rad_mol_xyz> [engine]
    eprtools iHFC_fromxyz         <file> <radicals> <depth>
    eprtools bonds2npz            <npz_file>
    eprtools molid2npz            <npz_file>
    eprtools addfile2npz          <npz_file_ref> <npz_file_add> <file_name>

Shell scripts
-------------

.. code-block:: none

    eprtools extract_bonds_vmd    <molecule.xyz>
    eprtools extract_EPRspec      [args...]
    eprtools gval_workflow        [args...]
    eprtools gval_dataset         [args...]
    eprtools gval_postpro         [args...]
    eprtools gval_data_restart    [args...]
    eprtools gvals_template       [args...]
    eprtools spectrum_from_gval   [args...]

Other files
-----------

Print the path to a bundled file::

    eprtools create_mol_png       # prints path to create_mol_png.tcl
