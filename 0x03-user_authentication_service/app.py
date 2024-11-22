#!/usr/bin/env python3
"""flask app"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth


app = Flask(__name__)
app.url_map.strict_slashes = False

AUTH = Auth()


@app.route("/", methods=["GET"])
def index() -> str:
    """homepage payload"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """method to handle login"""
    email, password = request.form.get("email"), request.form.get("password")

    if not email or not password:
        abort(401)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """method to handle logout"""
    cookie = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(cookie)

    if not user:
        abort(403)
    else:
        AUTH.destroy_session(user.id)
        return redirect("/")


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """profile route"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        return abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """reset password route"""
    email = request.form.get("email")
    if not email:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    else:
        return jsonify({"email": email, "reset_token": reset_token}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
