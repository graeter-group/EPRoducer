# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import importlib.util
import os
import sys

# importing path to the package and to the documentation tools
sys.path.insert(0, os.path.abspath('../src'))
sys.path.insert(0, os.path.abspath('.'))

# documentation of the shell scripts, generated from their help messages
from generate_script_docs import generate_script_docs  # noqa: E402

generate_script_docs()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'EPRoducer'
copyright = '2026, Daniel Sucerquia'
author = 'Daniel Sucerquia'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.napoleon',
              'sphinx.ext.viewcode',
              'sphinx.ext.intersphinx',
              'sphinx.ext.mathjax',
              'sphinx.ext.githubpages']

templates_path = ['_templates']
# the help messages of the scripts are not pages by themselves, they are
# included in modules/eproducer.rst
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store',
                    'modules/bash_rsts_doc/*']

autosummary_generate = True
autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'private-members': False,
    'show-inheritance': True,
}
# dependencies that are not installed are mocked, so that the API pages can
# be built anyway
autodoc_mock_imports = [module for module in ['numpy', 'scipy', 'matplotlib',
                                              'ase', 'networkx', 'pandas',
                                              'PlottingTool']
                        if importlib.util.find_spec(module) is None]

napoleon_google_docstring = False
napoleon_numpy_docstring = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable', None),
    'scipy': ('https://docs.scipy.org/doc/scipy', None),
    'matplotlib': ('https://matplotlib.org/stable', None),
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_title = 'EPRoducer'
# the logo already contains the name of the package (logo_only). Its drawing is
# black, so the header of the sidebar is white.
html_logo = '_static/logo.png'
# square icon made from the drawing of the logo, without the name
html_favicon = '_static/favicon.ico'

html_theme_options = {
    'logo_only': True,
    'style_nav_header_background': '#ffffff',
    'navigation_depth': 3,
    'titles_only': False,
    'style_external_links': True,
}

# Add custom CSS file
html_css_files = [
    'custom.css',
]
