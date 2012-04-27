# -*- coding: utf-8 -*-

import unittest

from mock import Mock
from nose.tools import eq_

from gg.core import (SSH_REMOTE, HTTPS_REMOTE,
                     extract_username_and_repo)

def test_extract_username_and_repo():
    args = {
        'user': 'alejandrogomez',
        'repo': 'gg',
    }
    https_url = HTTPS_REMOTE.format(**args)
    user, repo = extract_username_and_repo(https_url)
    eq_(user, args['user'])
    eq_(repo, args['repo'])
    ssh_url = SSH_REMOTE.format(**args)
    user, repo = extract_username_and_repo(ssh_url)
    eq_(user, args['user'])
    eq_(repo, args['repo'])
    


if __name__ == '__main__':
    unittest.main()
