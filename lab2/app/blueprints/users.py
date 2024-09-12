from flask import Blueprint, jsonify, session
from app.models import User
from app import db

bp = Blueprint("users", __name__, url_prefix="/users")


@bp.route("/", methods=["GET"])
def list():
    if not session.get("username"):
        return jsonify({"error": "You must login first"}), 401
    user = User.query.filter_by(username=session["username"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.role != "admin":
        return jsonify({"error": "You don't have permission to list users"}), 403

    normal_users = User.query.filter_by(role="user").all()

    return jsonify(normal_users), 200


@bp.route("/<int:user_id>", methods=["DELETE"])
def delete(user_id):
    if not session.get("username"):
        return jsonify({"error": "You must login first"}), 401
    user = User.query.filter_by(username=session["username"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if user.role != "admin":
        return jsonify({"error": "You don't have permission to delete this user"}), 403

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    else:
        db.session.delete(user)
        db.session.commit()

    return jsonify({"error": "User deleted"}), 200
