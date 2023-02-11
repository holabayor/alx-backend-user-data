#!/usr/bin/env python3
""" Session Expiraton Module
"""
from typing import TypeVar
import uuid
from models.user import User
from .session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    '''
        Session Expiration class
    '''

    def __init__(self):
        ''' Initialization
        '''
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id: str = None) -> str:
        ''' creates a Session ID for a user_id
        Returns: Session ID
        '''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {'user_id': user_id,
                                                  'created_at': datetime.now()}
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' User ID for Session ID
        Returns: User ID
        '''
        if session_id is None:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        if int(self.session_duration) <= 0:
            return session_dict.get('user_id')
        if session_dict.get('created_at') is None:
            return None
        session_time = session_dict.get(
            'created_at') + timedelta(seconds=self.session_duration)
        if (session_time < datetime.now()):
            return None
        return session_dict.get('user_id')
