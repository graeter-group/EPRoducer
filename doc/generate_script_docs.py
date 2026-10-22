"""
Generates the documentation of the shell scripts (and the other non-python
files) of EPRoducer. For each script, it writes two files in doc/modules:

- bash_rsts_doc/<name>.rst: the help message of the script (the text printed
  by its print_help function) or, if it does not have one, its leading
  comments. These files are included in modules/eproducer.rst.
- bash_rsts_scripts/<name>.rst: a page with the source code of the script.

The help messages are read from the files instead of running the scripts with
-h, because some scripts (e.g. gvals_template.sh) do not have a help flag.

It runs automatically on every build (see conf.py), and can also be run
directly with 'python generate_script_docs.py' from the doc directory.
"""

import os
import re
import sys
from pathlib import Path

DOC_DIR = Path(__file__).resolve().parent
PKG_DIR = DOC_DIR.parent / 'src' / 'eproducer'
MOD_DIR = DOC_DIR / 'modules'
LANGUAGES = {'.sh': 'bash', '.tcl': 'tcl'}


def help_message(path):
    """
    Extracts the help message of a script.

    Parameters
    ==========
    path: pathlib.Path
        path to the script.

    Return
    ======
    (str) text printed by the print_help function of the script or, if it
    does not have one, its leading comments.
    """
    lines = path.read_text().splitlines()
    for i, line in enumerate(lines):
        if re.match(r'\s*print_help\s*\(\)', line):
            # the message is the text of the first 'echo "' of the function,
            # up to the line with the closing quote
            start = next(j for j in range(i, len(lines))
                         if re.match(r'\s*echo (-e )?"', lines[j]))
            text = [re.sub(r'\s*echo (-e )?"', '', lines[start], count=1)]
            for line in lines[start + 1:]:
                if line.strip() == '"':
                    break
                text.append(line)
            text = '\n'.join(text)
            return text.replace('\\$', '$').replace('\\"', '"')

    comments = []
    for line in lines:
        if line.startswith('#!'):
            continue
        if not line.startswith('#'):
            break
        comments.append(line.lstrip('#').strip())
    return '\n'.join(comments)


def title(text):
    """
    Returns text as a reStructuredText title with over- and underline.
    """
    return f'{"=" * len(text)}\n{text}\n{"=" * len(text)}\n'


def doc_block(path):
    """
    Returns the content of bash_rsts_doc/<name>.rst for the script in path.
    """
    name = path.stem
    rel = path.relative_to(PKG_DIR.parent).as_posix()
    help_lines = help_message(path).strip('\n').splitlines()
    body = '\n'.join(('      ' + line).rstrip() for line in help_lines)
    return (f'\n{title(name)}\n'
            '.. container:: bash-script-title\n\n'
            f'   :ref:`[script] <script-{name}>` **{rel}**\n\n'
            '.. container:: bash-script-doc\n\n'
            '   .. line-block::\n\n'
            f'{body}\n')


def script_page(path):
    """
    Returns the content of bash_rsts_scripts/<name>.rst for the script in
    path.
    """
    name = path.stem
    source = os.path.relpath(path, MOD_DIR / 'bash_rsts_scripts')
    return (f'.. _script-{name}:\n\n'
            f'{title(f"Script of EPRoducer {name}")}\n'
            f'.. literalinclude:: {Path(source).as_posix()}\n'
            f'   :language: {LANGUAGES[path.suffix]}\n')


def write_if_changed(path, content):
    """
    Writes content in path only if it changes, so that Sphinx does not rebuild
    pages that did not change.
    """
    if not path.exists() or path.read_text() != content:
        path.write_text(content)


def generate_script_docs():
    """
    Writes the documentation files of all the scripts of EPRoducer and removes
    the ones of scripts that do not exist anymore.

    Return
    ======
    (list) names of the documented scripts.
    """
    scripts = sorted(p for p in PKG_DIR.rglob('*')
                     if p.suffix in LANGUAGES and '__pycache__' not in p.parts)
    names = [p.stem for p in scripts]

    for subdir, builder in [('bash_rsts_doc', doc_block),
                            ('bash_rsts_scripts', script_page)]:
        out_dir = MOD_DIR / subdir
        out_dir.mkdir(parents=True, exist_ok=True)
        for script in scripts:
            write_if_changed(out_dir / f'{script.stem}.rst', builder(script))
        for old in out_dir.glob('*.rst'):
            if old.stem not in names:
                old.unlink()

    # every script should be included in the page of the package
    package_page = (MOD_DIR / 'eproducer.rst').read_text()
    for name in names:
        if f'bash_rsts_doc/{name}.rst' not in package_page:
            print(f'WARNING: {name} is not included in modules/eproducer.rst',
                  file=sys.stderr)

    return names


if __name__ == '__main__':
    print('documented scripts:', ', '.join(generate_script_docs()))
