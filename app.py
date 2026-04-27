from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

DATA_FILE = "users.json"

def read_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            content = f.read().strip()
            return json.loads(content) if content else []
        except json.JSONDecodeError:
            return []

def write_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)


@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    users = read_users()

    new_user = {
        "id": int(datetime.now().timestamp() * 1000),
        "name": data.get("name"),
        "email": data.get("email")
    }

    users.append(new_user)
    write_users(users)

    return jsonify(new_user), 201


@app.route('/users', methods=['GET'])
def get_users():
    users = read_users()
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    users = read_users()

    for user in users:
        if user["id"] == user_id:
            user["name"] = data.get("name", user["name"])
            user["email"] = data.get("email", user["email"])
            write_users(users)
            return jsonify(user)

    return jsonify({"message": "User not found"}), 404


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    users = read_users()

    updated_users = [u for u in users if u["id"] != user_id]

    if len(users) == len(updated_users):
        return jsonify({"message": "User not found"}), 404

    write_users(updated_users)
    return jsonify({"message": "User deleted"})


if __name__ == '__main__':
    app.run(debug=True) 