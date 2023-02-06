#!/usr/bin/env python3
""" Module of Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    '''
        API class
    '''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''
            require auth
        '''
        return False

    def authorization_header(self, request=None) -> str:
        '''
            Auth header
        '''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''
            Current User
        '''
        return None
