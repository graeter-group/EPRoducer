
======
basics
======

.. container:: bash-script-title

   :ref:`[script] <script-basics>` **eproducer/basics.sh**

.. container:: bash-script-doc

   .. line-block::

      This script contains basics tools for other bash scripts. With the code in
      here, you can use the next functions

      - <first_argument> Add a label in every output of each bash script by giving
        it as a first argument.
      - <second_argument> Add anything in order to have verbose printing in the
        output. otherwise, the your script will ignore all the verbose.
      - adjust <text>: add the label and print what <text> in an adjusted column of
        80 characters.
      - verbose <text>: besides of the label, it adds the keyword VERBOSE in to the
        begining of <text> and print the adjusted text.
      - warning <text>: besides of the label, it adds the keyword WARNING in to the
        begining of <text> and print the adjusted text.
      - finish <text>: besides of the label, it use verbose to print <text> of the
        word "finish" if <text> is not given. It also stops the script with 'exit 0'
      - fail <text>: besides of the label, it adds the keyword VERBOSE in to the
        begining of <text> and print the adjusted text. It also print the message
        in the std_error and stops the script with 'exit 1'
      - load_modules: loads the modules I need in my codes when running in a cluster.
