#!/usr/bin/env python3
""" Session Expiraton Module
"""
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    '''
        Session Expiration class
    '''

    def create_session(self, user_id: str = None) -> str:
        ''' creates a Session ID for a user_id
        Returns: Session ID
        '''
        user_session = UserSession()
        session_id = super().create_session(user_id)
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' User ID for Session ID
        Returns: User ID
        '''
        user_id = super().create_session(session_id)
        return user_id
