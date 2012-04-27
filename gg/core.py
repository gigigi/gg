# -*- coding: utf-8 -*-

"""
gg.core
~~~~~~~

The heart of `gg`.
"""

import re
from gettext import gettext as _

import pygithub3
from git import Repo, Remote
from git.exc import InvalidGitRepositoryError


# GitHub remotes
SSH_REMOTE = 'git@github.com:{user}/{repo}.git'
HTTPS_REMOTE = 'https://{user}@github.com/{user}/{repo}.git'

USER_REPO_REMOTE_REGEX = re.compile(r'.*[:/](?P<user>\w+)\/(?P<repo>\w+)\.git')

INFO_TEMPLATE = """{name}    {language} w: {watchers} f: {forks}

{description}

Last updated at {updated_at}."""

def extract_username_and_repo(remote):
    match = USER_REPO_REMOTE_REGEX.match(remote)
    if not match:
        return 

    try:
        user = match.group('user')
        repo = match.group('repo')
    except IndexError:
        return
    else:
        return user, repo


class GitHub(pygithub3.Github):
    """
    The interface to GitHub.
    """
    def __init__(self, *args, **kwargs):
        pygithub3.Github.__init__(self, *args, **kwargs)
        self._username = self.users.get().login

    def new_repo(self, 
                 repo_name, 
                 repo_path):
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

    def info(self, repo_path):
        try:
            repo = Repo(repo_path)
        except InvalidGitRepositoryError:
            print _("Looks like %s is not a git repo" % repo_path)
            exit(1)

        git_config = repo.config_reader()
        remotes = [section for section 
                           in git_config.sections() 
                           if 'remote' in section]

        # get user and repo values
        values = None
        for remote in remotes:
            try:
                remote_url = git_config.get(remote, 'url')
            except:
                continue
            else:
                values = extract_username_and_repo(remote_url)
                if values:
                    break

        if not values:
            print _("Unable to find a remote on GitHub")
            exit(2)

        # fetch repo info
        user, repo = values[0], values[1]
        gh_repo = self.repos.get(user=user, repo=repo)

        # print 
        defaults = ({
            'name': gh_repo.name,
            'description': gh_repo.description,
            'language': '',
            'watchers': gh_repo.watchers,
            'forks': gh_repo.forks,
            'updated_at': gh_repo.updated_at,
        })
        if gh_repo.language:
            defaults.update({
                'language': gh_repo.language,
            })
        print unicode(INFO_TEMPLATE).format(**defaults)
