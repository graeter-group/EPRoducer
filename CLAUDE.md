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


