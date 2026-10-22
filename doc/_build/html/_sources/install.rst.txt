Installation
============

Requirements
------------

* Python >= 3.9
* numpy
* scipy
* matplotlib
* ase
* networkx
* pandas
* PlottingTool

Install
-------

Clone the repository and install in editable mode::

    cd /path/to/EPRoducer
    pip install -e .

This also installs the ``eproducer`` command-line tool.
To verify::

    eproducer -h

.. _orca-setup:

ORCA and MATLAB set up
----------------------

The shell scripts of EPRoducer that run calculations (e.g. ``gval_workflow``,
``extract_EPRspec`` and ``spectrum_from_gval``) call ``load_modules``, which
sources ``$HOME/sw/load_modules.sh``. Create that file so that it makes the
next programs available:

* ORCA, used by ``gval_workflow``. The variable ``orca`` must point to the ORCA
  binary, e.g.

  .. code-block:: bash

      orca_path="<absolute path to the Orca directory>"
      export PATH=${orca_path}:$PATH
      export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$orca_path"

      orca="$orca_path/orca"

* MATLAB with `EasySpin <https://www.easyspin.org/>`_ in its path, used by
  ``extract_EPRspec`` and ``spectrum_from_gval`` (e.g. ``module load matlab``
  in a cluster).

``gval_postpro`` and ``extract_bonds_vmd`` also need ``vmd`` in your ``PATH``.

.. _build-doc:

Build the documentation
-----------------------

This documentation is built with Sphinx and the Read the Docs theme::

    pip install sphinx sphinx_rtd_theme
    cd doc
    make html

The HTML pages are written in ``doc/_build/html``. :code:`eproducer doc` does
this automatically when needed and opens the documentation in your web
browser. The pages of the shell
scripts (``doc/modules/bash_rsts_doc`` and ``doc/modules/bash_rsts_scripts``)
are generated from the scripts on every build by
``doc/generate_script_docs.py``, so they are always up to date. A new script
only has to be included in ``doc/modules/eproducer.rst``; the build prints a
warning for the scripts that are not.
