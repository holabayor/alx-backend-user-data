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
        Returns:
            True if the path is not in the list of strings excluded_paths
        '''
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        for _path in excluded_paths:
            if path == _path or path == _path[:-1] or\
                    path.startswith(_path.split('*')[0]):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        '''
            Auth header
        '''
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        '''
            Current User
        '''
        return None
