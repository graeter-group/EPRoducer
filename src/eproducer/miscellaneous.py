"""
General-purpose utilities: shell command execution and introspection
helpers.
"""

import subprocess
import inspect
from importlib import import_module


def output_terminal(cmd, print_output=True, skip_error=False, print_cmd=False,
                    **kwargs):
    """
    Runs a command in a terminal and returns its output.

    Parameters
    ==========
    cmd: str
        bash command to be executed in the terminal.
    print_output: bool. Default=True
        True for printing the output (without empty lines) besides of
        returning it.
    skip_error: bool. Default=False
        True for continuing running although the command fails. Otherwise, an
        AssertionError with the error message is raised.
    print_cmd: bool. Default=False
        print the command before executing it.
    **kwargs:
        additional options for subprocess.Popen

    Return
    ======
    (str) standard output of the executed command.
    """
    if print_cmd:
        print(cmd)
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
            if print_output and len(output.strip()) != 0:
                print(output.strip())
    return_code = p.wait()

    if not skip_error:
        assert not return_code, f"ERROR executing the command \"{cmd}\"  " + \
            "with output_terminal with the next message:\n" + \
            p.stderr.read().strip()

    return out


def _time(keyword, logfile):
    """
    Used in eproducer.miscellaneous.time_g09. It extracts the time from a
    line of gaussian.

    Parameters
    ==========
    keyword:
        keyword that contains the line with the time you want to check.
    logfile:
        g09 log file containing the time information.

    Return
    ======
    (tuple) month (str), day, hour, minutes and seconds (int) written in the
    first line of logfile that contains keyword.
    """
    out = output_terminal("grep '" + keyword + "' " + logfile)
    out = out.split()
    start = out.index('at')

    month = out[start + 2]
    day = int(out[start + 3])
    time = out[start + 4].split(':')
    hour = int(time[0])
    minu = int(time[1])
    seco = int(time[2])

    return month, day, hour, minu, seco


# add2executable
def time_g09(logfile):
    """
    Function that extracts the time spend for one gaussian simulation from a
    .log file.

    Parameters
    ==========
    logfile: string
        .log file obtained during a gaussian simulation.

    Return
    ======
    (float) Time in minutes. The time in seconds, minutes and hours is also
    printed. If the simulation starts and ends in different months, it only
    prints a message and returns None.
    """
    t_i = _time('Leave Link    1', logfile)
    t_f = _time('Normal termination of Gaussian', logfile)

    if t_i[0] == t_f[0]:
        days = (t_f[1] - t_i[1]) * 24 * 3600
        hours = (t_f[2] - t_i[2]) * 3600
        minus = (t_f[3] - t_i[3]) * 60
        secos = t_f[4] - t_i[4]
        total = days + hours + minus + secos

        print("Time in seconds= ", total)
        print("Time in minutes= ", total / 60)
        print("Time in hours= ", total / 3600)

        return total / 60

    else:
        print('sorry, I cannot help you, modify me to compute \
            changes of months')


# add2executable
def optimized_e(file):
    """
    This code finds the last energy in a log file of gaussian computed using
    RBMK functional. The output is given in eV.

    Parameters
    ==========
    file: str
        log gaussian file.

    Return
    ======
    (float) Potential energy in eV units.
    """
    out = output_terminal('grep "E(RBMK) =" ' + file, print_output=False)
    energy = float(out.split()[-5])
    return energy * 27.2114  # energy in eV


# add2executable
def args_and_defaults(module, *args):
    """
    Takes a function and returns its parameters with their default values.

    Parameters
    ==========
    module: str
        name of the module containing the function, e.g.
        'eproducer.ase_utils.molecules'.
    *args: str
        path to the function inside the module, e.g. 'MoleculeSetter',
        'rot_x' for eproducer.ase_utils.molecules.MoleculeSetter.rot_x.

    Return
    ======
    (str) set of arguments and defaults.

    Notes
    -----
    moved to pkgdeveloper
    """
    # Deprecated
    module = import_module(module)

    method = getattr(module, args[0])
    for func in args[1:]:
        method = getattr(method, func)

    signature = inspect.signature(method)

    output = f"\n ### {args[-1]}\n"
    for param_name, param in signature.parameters.items():
        if param.default != inspect.Parameter.empty:
            output += f"{param_name}: Default={param.default}\n"
        else:
            output += f"{param_name}:\n"
    output += "\n"
    return output


# add2executable
def function_doc(module, *args):
    """
    Takes a function and returns its documentation.

    Parameters
    ==========
    module: str
        name of the module containing the function, e.g.
        'eproducer.ase_utils.molecules'.
    *args: str
        path to the function inside the module, e.g. 'MoleculeSetter',
        'rot_x' for eproducer.ase_utils.molecules.MoleculeSetter.rot_x.

    Return
    ======
    (str) function documentation

    Notes
    -----
    moved to pkgdeveloper
    """
    module = import_module(module)

    method = getattr(module, args[0])
    for func in args[1:]:
        method = getattr(method, func)

    return method.__doc__
