# -*- coding: utf-8 -*-

"""
gg.core
~~~~~~~

The heart of `gg`.
"""

from gettext import gettext as _

import pygithub3
from git import Repo, Remote


# GitHub remotes
SSH_REMOTE = 'git@github.com:{user}/{repo}.git'
HTTPS_REMOTE = 'https://{user}@github.com/{user}/{repo}.git'


class GitHub(pygithub3.Github):
    """
    The interface to GitHub.
    """
    def __init__(self, *args, **kwargs):
        pygithub3.Github.__init__(self, *args, **kwargs)
        self._username = self.users.get().login

    def new_repo(self, repo_name, repo_path):
        """Create a new repository and setup the remote on GitHub."""
        # initialize local repo
        repo = Repo.init(repo_path)

        # create GitHub repo
        name = repo_name.strip()
        try:
            self.repos.create(dict(name=name))
        except pygithub3.exceptions.UnprocessableEntity:
            # a repo with the given name exists already
            print _("Looks like you already have a repo called %s" % name)

        # add remotes
        template_args = dict(user=self._username, repo=repo_name)
        Remote.add(repo=repo, 
                   name='ssh', 
                   url=SSH_REMOTE.format(**template_args))
        Remote.add(repo=repo, 
                   name='https', 
                   url=HTTPS_REMOTE.format(**template_args))
