from datetime import datetime
import json
from pathlib import Path

from flask import Blueprint, jsonify, request

users_bp = Blueprint("users", __name__)

DATA_FILE = Path(__file__).resolve().parent.parent / "users.json"


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


@users_bp.route("/users", methods=["POST"])
def add_user():
    data = request.json or {}
    users = read_users()

    new_user = {
        "id": int(datetime.now().timestamp() * 1000),
        "name": data.get("name"),
        "email": data.get("email"),
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
