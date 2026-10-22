.. TODO: when the repository is public, uncomment the "Setup Pages" step in
   .github/workflows/jekyll-gh-pages.yml, so that this documentation is
   published on GitHub Pages. It is commented because GitHub Pages is not
   available while the repository is private.

.. _eproducer:

=========
EPRoducer
=========

**EPRoducer** is a set of tools to compute and analyze the EPR (Electron
Paramagnetic Resonance) parameters of radicals. It runs the ORCA calculations
of the g-values and hyperfine couplings, predicts the EPR spectra with
EasySpin, and finds which radical candidates, and in which proportions,
explain an experimental spectrum. All the tools are available from the
terminal as :code:`eproducer <function>` (see :doc:`cli`).

Workflow
--------

#. Prepare the structures of the radical candidates, by hand or from npz
   datasets (:mod:`eproducer.g_valsetup`).
#. Optimize them and compute their g-values, hyperfine couplings and
   frequencies with ORCA: :ref:`gval_workflow <doc-gval_workflow>`, or
   :ref:`gval_dataset <doc-gval_dataset>` for many radicals of npz datasets.
#. Predict the spectrum of each candidate with EasySpin:
   :ref:`extract_EPRspec <doc-extract_EPRspec>`.
#. Summarize the results and compare them with the experiments:
   :ref:`gval_postpro <doc-gval_postpro>` and :mod:`eproducer.postpro`.
#. Fit the experimental spectrum with the candidates: :mod:`eproducer.best_fit`.

The :doc:`tutorial <tutorials/EPRspectrum/tutorial_EPR>` goes through these
steps with a real example.

Package overview
----------------

- :doc:`eproducer <modules/eproducer>`

  - :mod:`~eproducer.g_valsetup`: structure utilities for the g-value
    calculations (connectivity, radical location, atoms for the hyperfine
    couplings, extraction of structures from npz datasets).
  - :mod:`~eproducer.postpro`: post-processing of the ORCA outputs (g-values,
    tables, comparison of spectra, bond dissociation enthalpies).
  - :mod:`~eproducer.best_fit`: fit of computed spectra to experimental ones.
  - :mod:`~eproducer.bonds2npz`: bonds and molecular IDs for npz datasets.
  - :mod:`~eproducer.miscellaneous`: shell command execution and other helpers.
  - :doc:`eproducer.ase_utils <modules/eproducer.ase_utils>`: molecular geometry
    tools built on top of ASE.
  - :doc:`eproducer.cli <modules/eproducer.cli>`: the :code:`eproducer` command.
  - :ref:`Shell scripts <shell-scripts>`: ORCA and EasySpin workflows and
    post-processing.

-------
Content
-------

.. toctree::
   :maxdepth: 2

   about
   install
   cli
   modules/eproducer
   tutorials/tutorials

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
