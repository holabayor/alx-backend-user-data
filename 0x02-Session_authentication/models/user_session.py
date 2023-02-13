#!/usr/bin/env python3
""" Session module
"""
from models.base import Base


class UserSession(Base):
    """ Session class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a Session instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
