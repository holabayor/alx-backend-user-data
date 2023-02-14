#!/usr/bin/env python3
"""
Authentication file
"""
from db import DB
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
import uuid
from user import User


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

    def register_user(self, email: str, password: str) -> User:
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

    def valid_login(self, email: str, password: str) -> bool:
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

    def create_session(self, email: str) -> str:
        """
        Create a session for a user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Get a user from a session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            user: User object
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a user's session.

        Args:
            user_id (int): The user ID.
        """
        print("To delete a session")
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        self._db.update_user(user.id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
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
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        '''
        Update a user's password.

        Args:
            reset_token (str): The reset password token.
            password (str): The new password.

        Returns:
            bool: True if the password was updated, False otherwise.
        '''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password)
        self._db.update_user(user.id, reset_token=None)
