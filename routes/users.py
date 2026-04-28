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


def next_user_id(users):
    numeric_ids = []
    for user in users:
        user_id = user.get("id")
        if isinstance(user_id, (int, float)):
            numeric_ids.append(int(user_id))
    return (max(numeric_ids) + 1) if numeric_ids else int(datetime.now().timestamp() * 1000)


@users_bp.route("/users", methods=["POST"])
def add_user():
    """
    Create a user
    ---
    tags:
      - Users
    summary: Create a user
    description: |
      Creates a new user with the given `name` and `email`.

      Returns the created user.

      If the request body is invalid, returns a 400 error.
      If the user already exists, returns a 400 error.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
          properties:
            name:
              type: string
              example: Ankur
            email:
              type: string
              example: ankur@example.com
    responses:
      201:
        description: User created
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1710000000000
            name:
              type: string
              example: Ankur
            email:
              type: string
              example: ankur@example.com
        examples:
          application/json:
            id: 1710000000000
            name: Ankur
            email: ankur@example.com
      400:
        description: Invalid request body
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json:
            message: name and email are required
    """
    data = request.json or {}
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"message": "name and email are required"}), 400

    users = read_users()

    new_user = {
        "id": next_user_id(users),
        "name": name,
        "email": email,
    }

    users.append(new_user)
    write_users(users)

    return jsonify(new_user), 201


@users_bp.route("/users", methods=["GET"])
def get_users():
    """
    List all users
    ---
    tags:
      - Users
    summary: List all users
    description: |
      Returns all users stored in the system.

      Each user contains `id`, `name`, and `email`.
    responses:
      200:
        description: List of users
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              name:
                type: string
              email:
                type: string
        examples:
          application/json:
            - id: 1710000000000
              name: Ankur
              email: ankur@example.com
            - id: 1710000000001
              name: Priya
              email: priya@example.com
    """
    users = read_users()
    return jsonify(users)


@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Update a user
    ---
    tags:
      - Users
    summary: Update a user
    description: |
      Updates the user with the given `id`.

      Returns the updated user.

      If the user is not found, returns a 404 error.
    parameters:
      - in: path
        name: user_id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Updated Name
            email:
              type: string
              example: updated@example.com
    responses:
      200:
        description: Updated user
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            email:
              type: string
        examples:
          application/json:
            id: 1710000000000
            name: Updated Name
            email: updated@example.com
      404:
        description: User not found
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json:
            message: User not found
    """
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
    """
    Delete a user
    ---
    tags:
      - Users
    summary: Delete a user
    description: |
      Deletes the user with the given `id`.

      Returns a success message.

      If the user is not found, returns a 404 error.
    parameters:
      - in: path
        name: user_id
        required: true
        type: integer
    responses:
      200:
        description: User deleted
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json:
            message: User deleted
      404:
        description: User not found
        schema:
          type: object
          properties:
            message:
              type: string
        examples:
          application/json:
            message: User not found
    """
    users = read_users()

    updated_users = [u for u in users if u["id"] != user_id]

    if len(users) == len(updated_users):
        return jsonify({"message": "User not found"}), 404

    write_users(updated_users)
    return jsonify({"message": "User deleted"})
