#!/usr/bin/env python3
""" Module of Authentication
"""
from .auth import Auth
from flask import request
from typing import List, TypeVar


class BasicAuth(Auth):
    '''
        API class
    '''
    pass
