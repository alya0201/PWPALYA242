from flask import Flask, jsonify, request


app = Flask(__name__)


users = [
    {"id": 1, "nama": "John", "email": "jhon@example.com"},
    {"id": 2, "nama": "Jane", "email": "jane@example.com"},
]

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({"users": users}), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next(
        (
            u for u in users if u["id"] == user_id
        ), None
    )
    if user:
        return jsonify({"user": user}), 200
    return jsonify({"message": "user not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = {
        "id": len(users) + 1,
        "nama": data["nama"],
        "email": data["email"],
    }
    users.append(new_user)
    return jsonify({"message": "Data berhasil ditambahkan", "user": new_user}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        data = request.get_json()
        user["nama"] = data.get("nama", user["nama"])
        user["email"] = data.get("email", user["email"])
        return jsonify({"message": "User updated", "user": user}), 200
    return jsonify({"message": "user not found"}), 404


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": "Data berhasil dihapus"}), 200

if __name__ == '_main_':
    app.run(debug=True)