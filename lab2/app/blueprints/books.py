from flask import Blueprint, session, redirect, url_for, render_template, request
from app.models import User, Book
from app import db

bp = Blueprint("books", __name__, url_prefix="/books")


@bp.route("/", methods=["GET", "POST"])
def list():
    if not session.get("username"):
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(username=session["username"]).first()
    if not user:
        return redirect(url_for("auth.login"))
    if request.method == "GET":
        return render_template("books/list.html", user=user)
    else:
        title = request.form["title"]
        cover = request.files["cover"]

        book = Book(title=title, cover=cover.read(), user_id=user.id)

        db.session.add(book)
        db.session.commit()
        return render_template("books/list.html", user=user)


@bp.route("/<int:book_id>", methods=["DELETE"])
def delete(book_id):\
    print(session.get("username"))
    if not session.get("username"):
        return redirect(url_for("auth.login"))
    user = User.query.filter_by(username=session["username"]).first()
    if not user:
        return redirect(url_for("auth.login"))
    book = Book.query.filter_by(id=book_id).first()
    if not book:
        return redirect(url_for("books.list"))
    if user.role != "admin" and book.user_id != user.id:
        return redirect(url_for("books.list"))
    else:
        if book:
            db.session.delete(book)
            db.session.commit()
    return redirect(url_for("books.list"))
