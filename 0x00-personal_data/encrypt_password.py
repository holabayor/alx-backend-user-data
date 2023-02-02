#!/usr/bin/env python3
'''
    Password Encryption
'''
import bcrypt


def hash_password(password: str) -> bytes:
    ''' function that expects one string argument name password
        Returns a salted, hashed password, which is a byte string.
    '''
    pwd = password.encode('utf-8')
    return bcrypt.hashpw(pwd, bcrypt.gensalt())
