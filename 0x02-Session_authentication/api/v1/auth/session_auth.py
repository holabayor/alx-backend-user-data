#!/usr/bin/env python3
""" Session Authentication
"""
import uuid
from .auth import Auth


class SessionAuth(Auth):
    '''
        Session Authentication class
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        ''' creates a Session ID for a user_id
        Returns:
        '''
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
