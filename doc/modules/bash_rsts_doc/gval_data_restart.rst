
=================
gval_data_restart
=================

.. container:: bash-script-title

   :ref:`[script] <script-gval_data_restart>` **eproducer/gval_data_restart.sh**

.. container:: bash-script-doc

   .. line-block::

      takes a list of xyz files and restarts the gval workflow for those files. This
      is useful when the previous run failed or was interrupted.

        -f  <file> file with list of xyz files to restart in the current directory.
        -p  <n processors> number of processors.
        -J  <job options> additional job options, e.g., "--partition=cpu".
        -P  use for preemptionable jobs.
        -o  add '-R' to restart, '-o' to avoid optimization or '-b' to avoid
            frequencies...

        -v  verbose.
        -h  prints this message.
