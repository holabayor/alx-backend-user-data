#!/usr/bin/env python3
'''
    Password Encryption
'''
import bcrypt


def hash_password(password: str) -> bytes:
    ''' function that expects one string argument name password
        Returns a salted, hashed password, which is a byte string.
    '''
    password = password.encode('utf-8')
    return bcrypt.hashpw(password, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    ''' function that expects 2 arguments and returns a boolean. '''
    password = password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)
