#!/usr/bin/env python3
"""
Main file
"""
from urllib import response
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """Test to Register a user with the given email and password.

    Args:
        email (str): The user's email address.
        password (str): The user's password.

    Returns:
        None
    """
    data = {"email": email,
            "password": password}
    response = requests.post(f'{URL}/users', data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    ''' Log in with the wrong password test
    Returns: None
    '''
    data = {"email": email,
            "password": password}
    response = requests.post(f'{URL}/sessions', data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    ''' Log in tester
    '''
    data = {"email": email,
            "password": password}
    response = requests.post(f'{URL}/sessions', data=data)
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies.get("session_id")


def profile_unlogged() -> None:
    ''' Test if the user is not logged in
    '''
    cookies = {"session_id": ""}
    response = requests.get(f'{URL}/profile', cookies=cookies)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    ''' Check if the user is logged on
    '''
    cookies = {"session_id": session_id}
    response = requests.get(f'{URL}/profile', cookies=cookies)
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    ''' Test the log out route and method
    '''
    cookies = {"session_id": session_id}
    response = requests.delete(f'{URL}/sessions', cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    ''' Test the reset password route and method
    '''
    data = {"email": email}
    response = requests.post(f'{URL}/reset_password', data=data)
    reset_token = response.json().get('reset_token')
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL,
                               "reset_token": reset_token}
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    data = {"email": email,
            "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(f'{URL}/reset_password', data=data)
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
