Description
-----------
This project aims to separate the section g_values of myutils (../myutils/src/myutils/g_values) into
a completely new python package.

rules
=====
- given that this package comes from myutils, there are many things from 'myutils'. The idea is
to do it completely independent which means that there should not be any call of 'myutils'
at all. Instead, copy ONLY the necessary methods, functions, classes from myutils un a local script.
- the user must be able to use the tool with the commandline 'eproducer <function>'
- never commit the changes by yourself. I will do it myself.

Project notes (work done with Claude, 2026-10-21 to 2026-10-29)
================================================================

Naming and history
------------------
- Display/pip name **EPRoducer** (prose, titles, pyproject, Sphinx project, folder name).
  Python import and terminal command are lowercase: `import eproducer`, `eproducer <function>`.
- Formerly called `eprtools`; renamed on 2026-10-22 and the folder moved from
  `sw/eprtools` to `sw/EPRoducer`. The old name should not appear in the code or the docs.
- Source: `myutils/src/myutils/g_values`, plus helpers copied from `myutils/miscellaneous.py`
  and `myutils/ase_utils/molecules.py`. Last synced with myutils on 2026-10-21 (myutils commit
  f1d32f0). When syncing again, these differences are expected and must be kept: `myutils.*`
  imports become `eproducer.*` (plotters come from `PlottingTool`), `myutils <cmd>` becomes
  `eproducer <cmd>` in the scripts, the docstrings, and the bug fixes listed below (myutils
  still has those bugs).
- The git remote (origin = https://github.com/graeter-group/EPRoducer.git) was removed on
  2026-10-22 at the user's request.

Layout
------
- `src/eproducer/`: python modules (g_valsetup, postpro, best_fit, bonds2npz, miscellaneous,
  ase_utils/molecules, cli/main), shell scripts (`*.sh`) and `create_mol_png.tcl`.
- `bonds2npz.py` is not used by any other EPRoducer code: it prepares npz datasets (entries
  `bonds`, `molid`) read by `../FlowEPRMol/flowmol/data_processing/process_geom.py`.
- `doc/`: Sphinx documentation modeled on `../myutils/doc` (layout) and `../sith/doc` (logo).
- `README.md` (logo + short description), `.github/workflows/jekyll-gh-pages.yml` (GitHub Pages).

Command line (`src/eproducer/cli/main.py`)
------------------------------------------
- Commands are registered in the dicts `pymodules`, `sh_executers` and `other_files`. A new
  script must also be included in `doc/modules/eproducer.rst`.
- Python commands: arguments before the first `--key` are strings split at the spaces; each
  `--key value` is evaluated as python and falls back to a string (`_eval_value`).
- `eproducer <script> args` joins the arguments with spaces and loses their quotes; use
  `$(eproducer <script> -path) ...` for values with spaces.
- `eproducer doc` builds the docs (`sphinx -M html`) only when a file in `doc/` or
  `src/eproducer/` is newer than `doc/_build/html/index.html`, then opens it with python's
  `webbrowser`; `eproducer doc -path` prints the path.

Shell scripts
-------------
- They load their helpers with `source "$(eproducer basics -path)" <label> $verbose`.
  `basics.sh` is a trimmed copy of myutils' one: adjust, verbose, warning, finish, fail and
  load_modules (sources `$HOME/sw/load_modules.sh`, which sets up g09, ORCA (`$orca`) and MATLAB).
- gval_workflow writes `<prior_name>_opt.xyz`, `_epr.out` and `_freq.out` (prior_name = model).
- gval_postpro: the paths given with `-e` are relative to each candidate directory
  (e.g. `../../experiments/exp.dat`) and are checked there; `-O` defaults to `epr_info.out`,
  so pass `-O model_epr.out` for gval_workflow outputs.
- gvals_template.sh is a template to copy (its `<replace: ...>` placeholders are a syntax
  error on purpose); it and extract_bonds_vmd.sh have no `-h`.

Documentation
-------------
- Build with `cd doc && make html` (needs sphinx and sphinx_rtd_theme) or `eproducer doc`.
- `doc/generate_script_docs.py` runs from `conf.py` at every build. It writes
  `doc/modules/bash_rsts_doc/<script>.rst` (help text read from `print_help`, or the leading
  comments) and `bash_rsts_scripts/<script>.rst` (source). It warns about scripts that are not
  included in `doc/modules/eproducer.rst`.
- Dependencies that cannot be imported (e.g. PlottingTool) are mocked by autodoc.
- nbsphinx/pandoc and sphinxcontrib-mermaid are not installed: the EPRfitter notebook is a
  download, and there are no mermaid diagrams.
- Logo: `doc/_static/logo.png` (`html_logo`, `logo_only`, white header because the drawing is
  black with an opaque white inside); `favicon.ico` was made from the drawing without the name.
  sith's `_templates/layout.html` was not copied: sphinx_rtd_theme 3.0.2 ignores it.
- `doc/_build` is tracked in git (the workflow runs `make clean html`). Test builds go into a
  scratch copy so that it is not changed by accident.
- GitHub Pages: the "Setup Pages" step of the workflow is commented until the repository is
  public (TODO at the top of `doc/index.rst`). The deploy job will probably also fail while
  the repository is private.

Tutorials (`doc/tutorials`)
---------------------------
- `EPRspectrum/tutorial_EPR.rst` was adapted from myutils, whose version was outdated: it uses
  `model_opt.xyz`/`model_epr.out`, computes the spectra with extract_EPRspec as a separate step,
  keeps the experiments at the project top level and uses `molecule.png`. It has not been run
  end to end with ORCA/MATLAB yet; the fit image and percentages come from the original
  myutils run. The `-f` indices (`g1,4d2`, `g1,4,6d2`) start from 1.
- `EPRfitter/tutorial_EPRfitter.ipynb` was re-executed with eproducer. Its fieldrange case gives
  a correlation of 0.70 (the 0.99 of myutils' saved output came from code older than
  2025-08-19); a note in the notebook explains it.

Bugs fixed on 2026-10-21/22 (myutils still has them)
---------------------------------------------------
1. `postpro.create_table_per_method`: crashed on return, truncated the labels, `\text{meth}` braces.
2. `best_fit.TheoMatchExpe.clean_candidates`: missing `return` in the recursive call.
3. `best_fit.create_fit_file` used `tme.field` (now `tme.fieldexp`); a stray `$` in the `find`
   pattern of `create_fit_file` and `fit_experiment`.
4. `postpro.extract_system_info`: inverted condition to draw the experimental lines.
5. CLI: plain strings after `--key` raised NameError (now `_eval_value`); gval_postpro had no
   default `orca_output`.
6. `TheoMatchExpe` keeps `fieldrange` in the refits (`self.fieldrange`); `best_fit` with `''`
   no longer crashes.
7. gval_postpro called `fail` before sourcing basics.sh; its `-e` check rejected valid paths.
8. (2026-11-03) spectrum_from_gval and extract_EPRspec: EasySpin 6.0.12's `pepper` gives wrong
   spectra when `hamsymm` returns Dinfh but the unique axis is not z (e.g. g = [a b b], or any
   rotated axial g from ORCA): the unique g component vanishes. Both scripts now pass
   `Opt.GridSymmetry = 'Ci'; Opt.GridFrame = eye(3);` to pepper when hamsymm returns Dinfh.

Open issues (not fixed)
-----------------------
- `create_mol_png.tcl` line 4: `f { $argc < 2 }` should be `if` (same in myutils).
- `g_valsetup.HFC_relevantA` raises IndexError when no H, O or N atom is found around the
  radicals (empty float array used as index).
- `doc/cli.rst` refers to `:ref:build-doc`, which was removed from `install.rst` in commit
  dcb6b15: the only warning of the doc build.
- `best_fit.fit_theoretical` adds `self.shift` to a fieldrange that `fit_shifting` already
  shifted: possible double shift, not verified.
- The README logo is hard to see in GitHub's dark mode (transparent background).
- PlottingTool is not on PyPI; install it from https://github.com/Sucerquia/PlottingTool.

Environment and testing notes
-----------------------------
- Cluster "otter" with SLURM (partitions p/s/d/h/c.otter). Run ORCA calculations with sbatch,
  not on the login node.
- `bash -n` prints syntax errors but exits with 0 on this machine: check its output, not its
  exit code.
- Python's `webbrowser` falls back to `xdg-open` on the user's forwarded X display. In tests,
  set `BROWSER` to a fake script that succeeds, or patch `webbrowser.open`. Headless Firefox
  crashes on the login node.
- eproducer was not installed in the user's environment (2026-10-29). Without installing it,
  run the CLI with `PYTHONPATH=src python3 -c "from eproducer.cli.main import main; main()" ...`.


