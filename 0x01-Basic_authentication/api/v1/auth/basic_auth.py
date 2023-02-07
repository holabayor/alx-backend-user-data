#!/usr/bin/env python3
""" Basic Authentication
"""
from .auth import Auth


class BasicAuth(Auth):
    '''
        API class
    '''

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        ''' Base64 part method
        Return:
            - the Base64 part of the Authorization header for a Basic Auth
        '''
        if authorization_header is None or\
                not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]
