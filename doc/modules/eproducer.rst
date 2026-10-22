eproducer package
=================

.. automodule:: eproducer

Subpackages
-----------

.. toctree::
   :maxdepth: 4

   eproducer.ase_utils
   eproducer.cli

Submodules
----------

eproducer.g_valsetup
~~~~~~~~~~~~~~~~~~~~

.. automodule:: eproducer.g_valsetup
   :members:
   :undoc-members:
   :show-inheritance:

eproducer.postpro
~~~~~~~~~~~~~~~~~

.. automodule:: eproducer.postpro
   :members:
   :undoc-members:
   :show-inheritance:

eproducer.best_fit
~~~~~~~~~~~~~~~~~~

.. automodule:: eproducer.best_fit
   :members:
   :undoc-members:
   :show-inheritance:

eproducer.bonds2npz
~~~~~~~~~~~~~~~~~~~

.. automodule:: eproducer.bonds2npz
   :members:
   :undoc-members:
   :show-inheritance:

eproducer.miscellaneous
~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: eproducer.miscellaneous
   :members:
   :undoc-members:
   :show-inheritance:

.. _shell-scripts:

Shell scripts
-------------

The shell scripts run the calculations and the post-processing from the
terminal. Get the path of a script with :code:`$(eproducer <script> -path)` to
run it, copy it or submit it with :code:`sbatch`. The scripts with flags print
the help messages below when they are called with :code:`-h`. Click
:code:`[script]` to see the source code of a script.

.. toctree::
   :hidden:
   :glob:

   bash_rsts_scripts/*

g-value calculations
~~~~~~~~~~~~~~~~~~~~

.. _doc-gval_workflow:

.. include:: bash_rsts_doc/gval_workflow.rst

.. _doc-gval_dataset:

.. include:: bash_rsts_doc/gval_dataset.rst

.. _doc-gval_data_restart:

.. include:: bash_rsts_doc/gval_data_restart.rst

Spectra
~~~~~~~

.. _doc-extract_EPRspec:

.. include:: bash_rsts_doc/extract_EPRspec.rst

.. _doc-spectrum_from_gval:

.. include:: bash_rsts_doc/spectrum_from_gval.rst

Post-processing
~~~~~~~~~~~~~~~

.. _doc-gval_postpro:

.. include:: bash_rsts_doc/gval_postpro.rst

.. _doc-gvals_template:

.. include:: bash_rsts_doc/gvals_template.rst

.. _doc-create_mol_png:

.. include:: bash_rsts_doc/create_mol_png.rst

Utilities
~~~~~~~~~

.. _doc-basics:

.. include:: bash_rsts_doc/basics.rst

.. _doc-extract_bonds_vmd:

.. include:: bash_rsts_doc/extract_bonds_vmd.rst
