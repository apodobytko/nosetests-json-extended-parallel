=======================
nosetests-json-extended-parallel
=======================

Creates json logging output for python nosetests unittest framework. Works with parallel testing (--processes=N)


Forked from nosetests-json-extended project and add support for running nosetest in parallel. 

.. _original_project: https://github.com/thschenk/nosetests-json-extended



The generated output can be used by the atom-nosetests_ plugin, which adds
python unit testing capability to the Atom_ editor.

 * This plugin is tested with python 2.7.8 and python 3.4.2.
 * This plugin is tested with virtualenv_.

.. _atom-nosetests: https://github.com/thschenk/atom-nosetests
.. _Atom: https://atom.io
.. _virtualenv: https://virtualenv.pypa.io/en/latest/

Install
-------

First install the package:

::

    pip install nosetests-json-extended-parallel


It is also possible to install the development version:

::

    git clone git@github.com:ruivapps/nosetests-json-extended-parallel.git
    pip install nosetests-json-extended-parallel


Usage
-----

Normal usage:

::

    nosetests --with-json-extended-parallel

This will automatically generate a file ``nosetests.json`` in the current working
directory.


For python3, replace ``nosetests`` with ``nosetests3``, or use the following form:

::

    python3 -m nose --with-json-extended-parallel
