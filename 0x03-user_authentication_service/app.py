#!/usr/bin/env python3
"""App module"""
from flask import Flask, jsonify, request, abort,\
    make_response, redirect, url_for
from auth import Auth
AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=['GET'], strict_slashes=False)
def index():
    """Index route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """Create a new user"""
    email = request.form.get("email")
    password = request.form.get('password')

    if email is None or email == "":
        return jsonify({"error": "email is required"}), 400

    if password is None or password == "":
        return jsonify({"error": "password is required"}), 400

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def sessions():
    """Authenticates user and creates a new session"""
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response(
            jsonify({"email": f"{email}",
                     "message": "logged in"}))
        response.set_cookie("session_id", session_id)
        return response
    abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Logout user from the app"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for("index"))


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """Returns user profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": f"{user.email}"})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """generate a token"""
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """generate a token"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": f"{email}", "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
