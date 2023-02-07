#!/usr/bin/env python3
""" Basic Authentication
"""
from .auth import Auth
from flask import request
from typing import List, TypeVar


class BasicAuth(Auth):
    '''
        API class
    '''

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        if authorization_header is None or\
                not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]
