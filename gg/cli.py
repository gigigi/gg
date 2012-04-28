# -*- coding: utf-8 -*-

"""
gg.cli
~~~~~~

Command line interface.
"""

from gettext import gettext as _
from argparse import ArgumentParser
from os import getcwd, path
import sys

from gg import __name__, __version__, __doc__
from gg.auth import authenticate
from gg.core import GitHub

CWD = getcwd()

# login
username, password = authenticate()
gh = GitHub(login=username, password=password)


# arg parser
parser = ArgumentParser(prog=__name__,
                        description=__doc__)
subparsers = parser.add_subparsers(dest='command')


# init
init_parser = subparsers.add_parser('init',
                                    description=_('initialize an empty git repository'),)
init_parser.add_argument('repo_name',
                         nargs='?',
                         type=str,
                         help=_('The name of the repo that will be created'))
init_parser.set_defaults(repo_name=path.split(CWD)[-1])
init_parser.add_argument('repo_path',
                         nargs='?',
                         type=str,
                         help=_('The path to the directory in which the repo will be created'))
init_parser.set_defaults(repo_path=CWD)

                    
# info
info_parser = subparsers.add_parser('info',
                                     description=_('show information about a git repository in GitHub'),)
info_parser.add_argument('repo_path',
                         nargs='?',
                         type=str,
                         help=_('The path to the directory of the repo'))
info_parser.set_defaults(repo_path=CWD)

# fork
fork_parser = subparsers.add_parser('fork',
                                     description=_('fork a repository'),)
fork_parser.add_argument('author',
                          nargs='?',
                          type=str,
                          help=_('The author of the repo'))
fork_parser.set_defaults(author=None)
fork_parser.add_argument('repo',
                          type=str,
                          help=_('The name of the repo'))
fork_parser.add_argument('repo_path',
                          nargs='?',
                          type=str,
                          help=_('The path in which to store the repo'))
fork_parser.set_defaults(repo_path=None)

# clone
clone_parser = subparsers.add_parser('clone',
                                     description=_('clone a repository'),)
clone_parser.add_argument('author',
                          nargs='?',
                          type=str,
                          help=_('The author of the repo'))
clone_parser.set_defaults(author=None)
clone_parser.add_argument('repo',
                          type=str,
                          help=_('The name of the repo'))
clone_parser.add_argument('repo_path',
                          nargs='?',
                          type=str,
                          help=_('The path in which to store the repo'))
clone_parser.set_defaults(repo_path=None)

# version
version = "%s %s" % ( __name__, __version__)
parser.add_argument("-v", "--version", 
                    action="version", 
                    version=version,
                    help=_("show program version and exit"))


def main():
    if sys.argv[1:]:
        args = parser.parse_args(sys.argv[1:])
    else:
        parser.parse_args(['--help'])
        exit(0)

    repo_path = args.repo_path
    command = args.command
    
    if command == 'init':
        repo_name = args.repo_name
        gh.new_repo(repo_name, repo_path)
    elif command == 'info':
        gh.info(repo_path)
    elif command == 'fork':
        repo = args.repo
        author = args.author
        gh.fork(author, repo, repo_path)
    elif command == 'clone':
        repo = args.repo
        author = args.author
        gh.clone(author, repo, repo_path)



    exit(0)
