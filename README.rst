gg
==

A command line interface to glue together git and GitHub.

installation
============

This package is still in a pre-alpha state and is not published
in PyPI yet. For installation, download the source code and type:

::

    python setup.py install

usage
=====

The first time you use ``gg`` it will prompt for your GitHub username and
password. It stores them in ``~/.ggrc``.


The available commands are:

``init``::


    gg init [name [path]]

Creates a local git repo in ``path`` (which defaults to ``PWD``) and a
GitHub repo called ``name``.

Two remotes are created in the git repo: ``ssh`` and ``https``.


``fork``::

    gg fork author repo [path]

Forks ``repo`` and clones the fork into ``path``. The clone will have a 
``upstream`` remote with the original repo's url.


``clone``::

    gg clone [author] repo [path]

Makes a clone of ``author``s ``repo`` in ``path``. The default ``author`` is the
authenticating user.


``info``::

    gg info [path]

Prints information of the repo contained in ``path``. By default, it shows 
current directory repository's information.
