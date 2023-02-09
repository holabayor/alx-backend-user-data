#!/usr/bin/env python3
""" Session Authentication
"""
from typing import TypeVar
import uuid

from models.user import User
from .auth import Auth


class SessionAuth(Auth):
    '''
        Session Authentication class
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        ''' creates a Session ID for a user_id
        Returns: Session ID
        '''
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' User ID for Session ID
        Returns: User ID
        '''
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        '''
            Current User
        '''
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None

        return User.get(user_id)

    def destroy_session(self, request=None):
        '''
        deletes the user session / logout
        '''
        if request is None:
            return False
        if self.session_cookie(request) is None:
            return False
        session_id = self.session_cookie(request)
        if not self.user_id_for_session_id:
            return False
        del self.user_id_by_session_id[session_id]
        return True
