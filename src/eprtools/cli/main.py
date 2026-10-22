"""
Entry point of the 'eprtools' command. It exposes the python functions in
pymodules, the shell scripts in sh_executers and the bundled files in
other_files as 'eprtools <function> [args...]'.
"""

from importlib import import_module
import subprocess
from pathlib import Path
import sys
import numpy as np


def output_terminal(cmd, print_output=True, skip_error=False, **kwargs):
    """
    Runs a command in a terminal and prints its output while it runs.

    Parameters
    ==========
    cmd: str
        bash command to be executed in the terminal.
    print_output: bool. Default=True
        True for printing the output besides of returning it.
    skip_error: bool. Default=False
        True for continuing running although the command fails.
    **kwargs:
        additional options for subprocess.Popen

    Return
    ======
    (str) standard output of the executed command.
    """
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         text=True,
                         **kwargs)
    out = ""
    output = ""
    while not (output == '' and p.poll() is not None):
        output = p.stdout.readline()
        if output:
            out += output
            if print_output:
                print(output, end="")
    return_code = p.wait()
    if not skip_error:
        assert not return_code, f"ERROR executing \"{cmd}\":\n" + \
            p.stderr.read().strip()
    return out


pymodules = {
    'compute_bde': 'eprtools.postpro',
    'add_gval2npz': 'eprtools.postpro',
    'extract_system_info': 'eprtools.postpro',
    'create_table_per_system': 'eprtools.postpro',
    'create_table_per_method': 'eprtools.postpro',
    'extract_gvals': 'eprtools.postpro',
    'nrand_rad': 'eprtools.g_valsetup',
    'ext_xyz_from_npz': 'eprtools.g_valsetup',
    'heavya_idx_from_ref': 'eprtools.g_valsetup',
    'rad_loc': 'eprtools.g_valsetup',
    'iHFC_fromxyz': 'eprtools.g_valsetup',
    'molid2npz': 'eprtools.bonds2npz',
    'bonds2npz': 'eprtools.bonds2npz',
    'addfile2npz': 'eprtools.bonds2npz',
    'mat2dat': 'eprtools.best_fit',
    'best_fit': 'eprtools.best_fit',
    'spect_w_experiment': 'eprtools.best_fit',
    'create_fit_file': 'eprtools.best_fit',
}

sh_executers = {
    'basics': './basics.sh',
    'extract_bonds_vmd': './extract_bonds_vmd.sh',
    'extract_EPRspec': './extract_EPRspec.sh',
    'gval_data_restart': './gval_data_restart.sh',
    'gval_dataset': './gval_dataset.sh',
    'gval_postpro': './gval_postpro.sh',
    'gvals_template': './gvals_template.sh',
    'gval_workflow': './gval_workflow.sh',
    'spectrum_from_gval': './spectrum_from_gval.sh',
}

other_files = {
    'create_mol_png': './create_mol_png.tcl',
}


def _eval_value(value):
    """
    Evaluates the value of a '--<key> <value>' terminal argument as a python
    expression. If it is not a valid expression (e.g. a file name like
    epr_info.out), the value is returned as a string.

    Parameters
    ==========
    value: str
        value given in the terminal.

    Return
    ======
    evaluated value, or the value itself (str) without surrounding spaces.
    """
    try:
        return eval(value)
    except Exception:
        return value.strip()


def _read_arguments():
    """
    Reads the arguments given in the terminal after the name of the function.
    The arguments before the first '--<key>' are passed as positional
    arguments (str). Each '--<key> <value>' is passed as a keyword argument
    whose value is evaluated as a python expression, e.g. '--n 3' gives n=3
    and "--selection '[1, 2]'" gives selection=[1, 2]. Values that are not
    valid python expressions, e.g. '--orca_output epr_info.out', are passed
    as strings (see _eval_value).

    Return
    ======
    (tuple) (args, kwargs) with the list of positional arguments and the
    dictionary of keyword arguments.
    """
    if len(sys.argv) == 1:
        return ((), {})
    argument = '_reader_args'
    values = ''
    args_dict = {}
    for entry in np.array(sys.argv[1:]):
        if '--' == entry[:2]:
            if argument == '_reader_args':
                args_dict[argument] = values.split(" ")[2:]
                argument = entry.replace('--', '')
                values = ''
            else:
                args_dict[argument] = _eval_value(values)
                argument = entry.replace('--', '')
                values = ''
        else:
            values += ' ' + entry
    if argument == '_reader_args':
        args_dict[argument] = values.split(" ")[2:]
    else:
        args_dict[argument] = _eval_value(values)
    args = args_dict['_reader_args']
    del args_dict['_reader_args']

    if '--' == sys.argv[1][:2]:
        args = ()

    return (args, args_dict)


def main():
    """
    Runs each time eprtools is called from the terminal. Depending on the
    first argument, it prints the list of functions (-h), runs a python
    function, runs a shell script or prints the path of a bundled file.
    After the name of a python function, -h prints its docstring and -path
    its module. After the name of a shell script, -path prints the path of
    the script.

    Return
    ======
    (None)
    """
    if sys.argv[1] in ('-h', '--help', 'help'):
        functions = list(pymodules.keys()) + list(sh_executers.keys())
        functions.sort()
        print("\n'eprtools' contains the next set of tools:\n")
        for function in functions:
            print("    -   " + function)
        print("\nTo use one of the functions from the terminal, use:\n\n"
              "  'eprtools <function> <arg1> <arg2>...'\n\n"
              "For detailed information of any function, use \"-h\" as first"
              " argument (<arg1>).")

    elif sys.argv[1] in pymodules.keys():
        module = import_module(pymodules[sys.argv[1]])
        method = getattr(module, sys.argv[1])
        if '-h' in sys.argv:
            print(method.__doc__)
        elif '-path' in sys.argv:
            print(pymodules[sys.argv[1]])
        else:
            arguments = _read_arguments()
            output = method(*arguments[0], **arguments[1])
            if output is not None:
                print(output)

    elif sys.argv[1] in sh_executers.keys():
        pkg_dir = str(Path(__file__).parent.parent)
        if '-path' in sys.argv[2:]:
            print(pkg_dir + '/' + sh_executers[sys.argv[1]][2:])
        else:
            command = pkg_dir + '/' + sh_executers[sys.argv[1]][2:] + \
                ' ' + ' '.join(sys.argv[2:])
            output_terminal(command, print_output=True)

    elif sys.argv[1] in other_files.keys():
        pkg_dir = str(Path(__file__).parent.parent)
        print(pkg_dir + '/' + other_files[sys.argv[1]][2:])

    elif sys.argv[1] == 'path':
        print(str(Path(__file__).parent.parent))

    else:
        print(f"ERROR: keyword '{sys.argv[1]}' not recognized. "
              "Use 'eprtools -h' to see the available options.")


if __name__ == "__main__":
    main()
