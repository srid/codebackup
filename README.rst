codebackup
==========

A simple command line tool to backup all of your Github and Bitbucket
repositories to the specified directory.

Installing
----------

Use one of the following commands (the later works in ActivePython)::

    $ sudo pip install codebackup
    
    $ pypm install codebackup

Usage
-----

::

    $ codebackup --github-user=srid --bitbucket-user=srid ~/Dropbox/codebackup

Credits
-------

- `github-simple-backup`_, original inspiration
- `Distribute`_
- `Buildout`_
- `modern-package-template`_

.. _`github-simple-backup`: http://github.com/jbalogh/github-simple-backup
.. _Buildout: http://www.buildout.org/
.. _Distribute: http://pypi.python.org/pypi/distribute
.. _`modern-package-template`: http://pypi.python.org/pypi/modern-package-template
