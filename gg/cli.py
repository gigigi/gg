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

    command = args.command
    
    if command == 'init':
        repo_path = args.repo_path
        repo_name = args.repo_name
        gh.new_repo(repo_name, repo_path)
    elif command == 'info':
        repo_path = args.repo_path
        gh.info(repo_path)


    exit(0)
