# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.dirname(TEST_DIR)
sys.path.insert(0, ROOT_DIR)

from unittest import main, TestCase
from douban_client import DoubanClient
from douban_client.api.error import DoubanAPIError

try:
    from local_config import KEY, SECRET, CALLBACK, SCOPE, TOKEN
except ImportError:
    KEY = ''
    SECRET = ''
    CALLBACK = ''

    SCOPE_MAP = { 'basic': ['douban_basic_common', 'community_basic_user'], }
    
    try:
        from functools import reduce
        SCOPE = ','.join(reduce(lambda x, y: x + y, list(SCOPE_MAP.values())))
    except ImportError:
        SCOPE = ','.join(reduce(lambda x, y: x + y, SCOPE_MAP.values()))

    TOKEN = ''

def get_client():
    client = DoubanClient(KEY, SECRET, CALLBACK, SCOPE)

    token = TOKEN

    if token:
        client.auth_with_token(token)
    else:
        print('Go to the following link in your browser:')
        print(client.authorize_url)

        code = raw_input('Enter the verification code and hit ENTER when you\'re done:')
        client.auth_with_code(code)
        print('token code:', client.token_code)
        print('refresh token code:', client.refresh_token_code)
    return client

client = get_client()

class DoubanClientTestBase(TestCase):
    def setUp(self):
        pass

    @property
    def client(self):
        return client
