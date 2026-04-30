from datetime import datetime
import json
import os
from pathlib import Path

from flask import Blueprint, jsonify, request
import jwt

users_bp = Blueprint("users", __name__)

DATA_FILE = Path(__file__).resolve().parent.parent / "users.json"
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-key")
JWT_ALGORITHM = "HS256"


def read_users():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        try:
            content = f.read().strip()
            return json.loads(content) if content else []
        except json.JSONDecodeError:
            return []


def write_users(users):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)


def next_user_id(users):
    numeric_ids = []
    for user in users:
        user_id = user.get("id")
        if isinstance(user_id, (int, float)):
            numeric_ids.append(int(user_id))
    return (max(numeric_ids) + 1) if numeric_ids else int(datetime.now().timestamp() * 1000)


@users_bp.route("/users", methods=["POST"])
def add_user():
    data = request.json or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if not name or not email or not password:
        return jsonify({"message": "name, email and password are required"}), 400

    users = read_users()

    new_user = {
        "id": next_user_id(users),
        "name": name,
        "email": email,
        "password": password,
    }

    users.append(new_user)
    write_users(users)

    return jsonify(new_user), 201


@users_bp.route("/users", methods=["GET"])
def get_users():
    users = read_users()
    return jsonify(users)


@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json or {}
    users = read_users()

    for user in users:
        if user["id"] == user_id:
            user["name"] = data.get("name", user["name"])
            user["email"] = data.get("email", user["email"])
            user["password"] = data.get("password", user.get("password", ""))
            write_users(users)
            return jsonify(user)

    return jsonify({"message": "User not found"}), 404


@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    users = read_users()

    updated_users = [u for u in users if u["id"] != user_id]

    if len(users) == len(updated_users):
        return jsonify({"message": "User not found"}), 404

    write_users(updated_users)
    return jsonify({"message": "User deleted"})


@users_bp.route("/login", methods=["POST"])
def login_user():
    data = request.json or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    users = read_users()
    matched_user = next(
        (
            user
            for user in users
            if user.get("email") == email and user.get("password") == password
        ),
        None,
    )
    print(matched_user)
    if not matched_user:
        return jsonify({"message": "Invalid email or password"}), 401

    now = datetime.utcnow()
    payload = {
        "sub": str(matched_user.get("id")),
        "email": matched_user.get("email"),
        "iat": int(now.timestamp()),
        "exp": int(now.timestamp()) + 3600,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return jsonify(
        {
            "token": token,
            "token_type": "Bearer",
            "expires_in": 3600,
            "user": {
                "id": matched_user.get("id"),
                "name": matched_user.get("name"),
                "email": matched_user.get("email"),
            },
        }
    )
