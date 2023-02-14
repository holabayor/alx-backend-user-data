#!/usr/bin/env python3
'''
Basic flask application
'''
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)

AUTH = Auth()


@app.route("/")
def hello():
    '''
    Basic hello world
    '''
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def create_user():
    '''
    Create a new user
    '''
    data = request.form
    email = data.get("email")
    password = data.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}",
                        "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    '''
    Log the user in
    '''
    data = request.form
    email = data.get("email")
    password = data.get("password")
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)

        response = jsonify({"email": f"{email}",
                            "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    '''
    Delete the session cookie and redirect
    '''
    session_id = request.cookies.get('session_id')
    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
        else:
            abort(403)
    else:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> str:
    '''
    Get the user profile
    '''
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST', 'PUT'])
def get_reset_password_token() -> str:
    '''
    Reset the user password
    '''
    if request.method == 'POST':
        data = request.form
        email = data.get("email")
        try:
            token = AUTH.get_reset_password_token(email)
            return jsonify({"email": f"{email}",
                            "reset_token": f"{token}"}), 200
        except Exception:
            abort(403)
    elif request.method == 'PUT':
        data = request.form
        email = data.get("email")
        reset_token = data.get("reset_token")
        new_password = data.get("new_password")
        try:
            AUTH.update_password(reset_token, new_password)
            return jsonify({"email": f"{email}",
                            "message": "Password updated"}), 200
        except Exception:
            abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
