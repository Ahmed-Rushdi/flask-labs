from flask import Blueprint, render_template, redirect, url_for, request, session
from app.models import User, Book

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/dashboard", methods=["GET"])
def dashboard():
    if not session.get("username"):
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(username=session["username"]).first()
    if not user or user.role != "admin":
        return redirect(url_for("home"))
    tab = request.args.get("tab", "books")
    if tab == "users":
        users = User.query.filter_by(role="user").all()
        return render_template("admin/dashboard.html", tab=tab, users=users)
    else:
        books = Book.query.all()
        return render_template("admin/dashboard.html", tab=tab, books=books)
