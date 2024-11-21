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
    return jsonify({"message", "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
