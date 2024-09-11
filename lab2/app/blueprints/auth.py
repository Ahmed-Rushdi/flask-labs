from flask import Blueprint, flash, render_template, request, redirect, url_for, session

from app import db
from app.models import User, Book

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("users/register.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["password-conf"]
        if password != confirm_password:
            flash("Passwords don't match", "danger")
            return redirect(url_for("auth.register"))

        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists", "danger")
            return render_template("users/register.html")
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        session["username"] = username
        return redirect(url_for("auth.profile"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("users/login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        username_in_db = User.query.filter_by(username=username).first()
        if not username_in_db or not username_in_db.verify_password(password):
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.login"))

        session["username"] = username
        return redirect(url_for("auth.profile"))


@bp.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect(url_for("auth.login"))


@bp.route("/profile", methods=["GET", "POST"])
def profile():
    username = session.get("username")
    if not username:
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(username=username).first()
    if request.method == "GET":
        return render_template(
            "users/profile.html",
            user=user,
        )
    else:
        avatar = request.files["avatar"]
        if avatar:
            user.avatar = avatar.read()
            db.session.commit()
        return redirect(url_for("auth.profile"))
