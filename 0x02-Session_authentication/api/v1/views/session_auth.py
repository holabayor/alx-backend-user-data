#!/usr/bin/env python3
""" Module of Session Authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login/',
                 methods=['POST'], strict_slashes=False)
def authenticate_session() -> str:
    """ GET /auth_session/login
    Return:
      - handles all routes for the Session authentication
    """
    user_email = request.form.get('email')
    user_pwd = request.form.get('password')
    if not user_email:
        return jsonify({"error": "email missing"}), 400
    if not user_pwd:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': user_email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(user_pwd):
            from api.v1.app import auth

            session_id = auth.create_session(user.id)
            SESSION_NAME = getenv('SESSION_NAME')
            response = jsonify(user.to_json())
            response.set_cookie(SESSION_NAME, session_id)
            return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout/', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """ GET /auth_session/logout
    Return:
      - deletes the user session / logout
    """
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
