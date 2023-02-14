#!/usr/bin/env python3
"""
Authentication file
"""
from db import DB
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
    Hash a password.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generate a UUID.

    Returns:
        str: The UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email, password):
        """Register a new user.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            user: User object
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(email, _hash_password(password))
            return user
        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email, password):
        """Check if a user is logged in.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the user is logged in, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email):
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session(self, session_id):
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id):
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        session_id = user.session_id
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email):
        '''
        Get a reset password token for a user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The reset password token.
        '''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_password=token)
        return token

    def update_password(self, reset_token, password):
        '''
        Update a user's password.

        Args:
            reset_token (str): The reset password token.
            password (str): The new password.

        Returns:
            bool: True if the password was updated, False otherwise.
        '''
        try:
            user = self._db.find_user_by(reset_password=reset_token)
        except NoResultFound:
            raise ValueError
        user.hashed_password = _hash_password(password)
        user.reset_token = None
