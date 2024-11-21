#!/usr/bin/env python3
"""flask app"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
app.url_map.strict_slashes = False

Auth = Auth()


@app.route("/", methods=["GET"])
def index() -> str:
    """homepage payload"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        Auth.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
