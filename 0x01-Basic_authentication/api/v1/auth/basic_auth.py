#!/usr/bin/env python3
""" Basic Authentication
"""
from base64 import b64decode
from typing import Tuple
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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str)\
            -> str:
        ''' Base64 part method
        Return:
            - decoded value of a Base64 string base64_authorization_header
        '''
        if base64_authorization_header is None or\
                not isinstance(base64_authorization_header, str):
            return None
        try:
            encoded = base64_authorization_header.encode('utf-8')
            decoded64 = b64decode(encoded)
            return decoded64.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> Tuple[str, str]:
        '''
        Return:
            the user email and password from the Base64 decoded value
        '''
        if decoded_base64_authorization_header is None or\
                not isinstance(decoded_base64_authorization_header, str) or\
                ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':'))
