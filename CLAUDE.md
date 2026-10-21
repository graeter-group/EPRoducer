Description
-----------
This project aims to separate the section sith of myutils (../myutils/src/myutils/g_vals) into
a completely new python package.

rules
=====
- given that this package comes from myutils, there are many things from 'myutils'. The idea is
to do it completely independent which means that there should not be any call of 'myutils'
at all. Instead, copy ONLY the necessary methods, functions, classes from myutils un a local script.
- the user must be able to use the tool with the commandline 'eprtools <function>'



