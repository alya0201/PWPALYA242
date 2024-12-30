from flask import Blueprint, jsonify, request
from . import db
from .models import User

main = Blueprint('main', __name__)

@main.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(
        [
            {"id": user.id,
             "name": user.name, 
             "email": user.email
            } 
            for user in users
        ]
    )

@main.route('/users/<int:user_id>', methods=['GET'])
def get_users(user_id):
    user = User.query.get(user_id)
    if user :
        return jsonify(
            {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
            for user in user
        )
    return jsonify({"message": "user not found"}), 404

@main.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({"message": "Name or email are required"}), 400

    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Users Created", 
                    "user": {
                        "id" : new_user.id, 
                        "name": new_user.name, 
                        "email": new_user.email
                    }
                    }), 201

@main.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)

    return jsonify({"message": "User updated", 
                    "user": {
                        "id" : user.id, 
                        "name": user.name, 
                        "email": user.email
                    }
                    }), 201