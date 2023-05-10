#!/usr/bin/env python3
"""App module"""
from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
