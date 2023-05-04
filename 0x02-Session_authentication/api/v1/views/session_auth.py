#!/usr/bin/env python3
""" Module of Sessions views
"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
import os


@app_views.route("/auth_session/login", methods=['POST'], strict_slashes=False)
def session_login():
    """session login"""
    user_email = request.form.get('email')
    user_pwd = request.form.get('password')

    if user_email is None or user_email == '':
        return jsonify({"error": "email missing"}), 400

    if user_pwd is None or user_pwd == '':
        return jsonify({"error": "password missing"}), 400

    from models.user import User
    current_user = None
    try:
        users = User.search({'email': user_email})
        if type(users) is list and len(users) > 0:
            for user in users:
                if user.is_valid_password(user_pwd):
                    current_user = user
            if current_user is None:
                return jsonify({"error": "wrong password"}), 401
    except KeyError:
        pass

    if current_user is None:
        return jsonify({"error": "no user found for this email"}), 404

    from api.v1.app import auth
    session_id = auth.create_session(current_user.id)
    session_name = os.getenv("SESSION_NAME")
    response = make_response(jsonify(user.to_json()))
    response.set_cookie(session_name, session_id)
    return response


@app_views.route("/auth_session/logout", methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    """logs a user out of session"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({})
