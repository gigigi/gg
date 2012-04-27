gg
==

A command line interface to glue together git and GitHub.


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


``info``::

    gg info [path]

Prints information of the repo contained in ``path``. By default, it shows 
current directory repository's information.
