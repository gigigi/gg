# -*- coding: utf-8 -*-

"""
gg.auth
~~~~~~~

This module contains the authentication logic.
"""

from ConfigParser import RawConfigParser
from gettext import gettext as _
from getpass import getuser, getpass
from os import getenv, path

from gg import __name__


HOME= getenv('HOME') 
CONFIG_FILE = path.join(HOME, '.%src' % __name__)

def authenticate():
    """
    Return a `username`, `password` tuple with the credentials. 
    
    If `gg` was started for the first time, it prompts for username and password 
    and stores them in `CONFIG_FILE`.
    """
    values = None
    if path.isfile(CONFIG_FILE):
        values = parse_credentials(CONFIG_FILE)

    if values:
        return values[0], values[1]
    return prompt_for_credentials()
    
def parse_credentials(config_file):
    """Parse credentials from `config_file`."""
    conf = RawConfigParser()
    conf.read(config_file)
    if conf.has_section('credentials') and \
        conf.has_option('credentials', 'username') and \
        conf.has_option('credentials', 'password'):
        username = conf.get('credentials', 'username')
        password = conf.get('credentials', 'password') 
        return username, password
    else:
        return None

def prompt_for_credentials():
    """Read credentials from standard input."""
    print _("What's your GitHub username?")
    username = raw_input()
    print _("And password?")
    password = getpass()
    save_credentials(username, password)
    return username, password

def save_credentials(username, password):
    """Save the credentials for `username`."""
    conf = RawConfigParser()
    conf.read(CONFIG_FILE)
    conf.add_section('credentials')
    conf.set('credentials', 'username', username)
    conf.set('credentials', 'password', password)

    with open(CONFIG_FILE, 'w') as config_file:
        conf.write(config_file)
