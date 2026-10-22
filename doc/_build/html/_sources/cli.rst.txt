Command-line interface
======================

``eproducer`` exposes Python functions and shell scripts through a unified CLI.
The general usage is::

    eproducer <command> [args...]

To list all the commands, use::

    eproducer -h

Pass ``-h`` after a Python command to print its docstring::

    eproducer <command> -h

Arguments of the Python commands
--------------------------------

The arguments before the first ``--<key>`` are passed to the function as
positional arguments (strings). They are split at the spaces, so they must not
contain spaces. Each ``--<key> <value>`` is passed as a keyword argument whose
value is evaluated as a Python expression when possible, and passed as a
string otherwise. These values can contain spaces::

    eproducer nrand_rad radicals.npz --n 2 --Nmin 5 --exclude "[1, 3]"
    eproducer extract_system_info PYD/ "[2.0062,2.0055,2.0022]" --orca_output model_epr.out

Python commands
---------------

g-value extraction and post-processing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: none

    eproducer extract_gvals        <orca_out>
    eproducer add_gval2npz         <path>
    eproducer extract_system_info  <sys_path> <exp_values> [--orca_output <file>]
    eproducer create_table_per_system  --experiment "[gx, gy, gz]" --systems "['<dir1>/', ...]" [--orca_file <file>]
    eproducer create_table_per_method  --data "<g-values and errors>" --experiment "[gx, gy, gz]" --methods "['<m1>', ...]"
    eproducer compute_bde          --reactants "['<r1.out>', ...]" --products "['<p1.out>', ...]"

Spectral fitting
~~~~~~~~~~~~~~~~

.. code-block:: none

    eproducer best_fit             <experiment> <output> <fieldrange> [files...]
    eproducer spect_w_experiment   <experiment> <theory> <output>
    eproducer create_fit_file      <output> [experiment_file] [basis_pattern] [basis_location]
    eproducer mat2dat              <file_field> <file_spectrum> <output>

Structure utilities
~~~~~~~~~~~~~~~~~~~

.. code-block:: none

    eproducer ext_xyz_from_npz     <npz_file> [--selection "[i, j, ...]"] [--create_xyz_files False]
    eproducer nrand_rad            <npz_file> [--n <n>] [--Nmin <N>] [--entry <entry>] [--exclude "[i, j, ...]"]
    eproducer heavya_idx_from_ref  <ref_mol_xyz> <rad_mol_xyz> <index> [engine]
    eproducer rad_loc              <ref_mol_xyz> <rad_mol_xyz> [engine]
    eproducer iHFC_fromxyz         <file> <radicals> <depth>
    eproducer bonds2npz            <npz_file>
    eproducer molid2npz            <npz_file>
    eproducer addfile2npz          <npz_file_ref> <npz_file_add> <file_name>

The documentation of each function is in :doc:`modules/eproducer`.

Shell scripts
-------------

.. code-block:: none

    eproducer gval_workflow        [flags...]
    eproducer gval_dataset         [flags...]
    eproducer gval_data_restart    [flags...]
    eproducer extract_EPRspec      [flags...]
    eproducer spectrum_from_gval   [flags...]
    eproducer gval_postpro         [flags...]
    eproducer extract_bonds_vmd    <molecule.xyz>
    eproducer gvals_template -path # template to copy, see the tutorial
    eproducer basics -path         # path to basics.sh, sourced by the scripts above

Add ``-path`` after the name of a script to print its path instead of running
it. This is useful to submit it with ``sbatch`` or to pass values that contain
spaces, because ``eproducer <script> ...`` joins the arguments with spaces and
loses their quotes::

    $(eproducer spectrum_from_gval -path) -g '[ 2.0 2.0 2.0 ]' -e experiment.dat

The flags of each script are described in :ref:`shell-scripts`.

Other files
-----------

Print the path to a bundled file::

    eproducer create_mol_png       # prints path to create_mol_png.tcl
    eproducer path                 # prints the path of the eproducer package

Documentation
-------------

Open this documentation in your web browser::

    eproducer doc                  # opens the html documentation
    eproducer doc -path            # prints the path of its index.html

The documentation is built first if it was not built yet or if its sources
or the package changed after the last build (see :ref:`build-doc`). If no
browser can be opened, e.g. in a cluster without a display, open the printed
file in your browser.
