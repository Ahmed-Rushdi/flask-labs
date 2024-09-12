from app import db
import bcrypt


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    cover = db.Column(db.BLOB, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __init__(self, title: str, cover: bytes, user_id: int) -> None:
        self.title = title
        self.cover = cover
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"<Book {self.id}, title: {self.title}>"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), unique=False, nullable=False)
    role = db.Column(db.String(30), unique=False, nullable=False)
    avatar = db.Column(db.BLOB, nullable=True)
    books = db.relationship("Book", backref="user", cascade="all, delete")

    def __init__(self, username: str, password: str, role: str = "user") -> None:
        self.username = username
        self.password = password
        self.role = role

    def __repr__(self) -> str:
        return f"<User {self.id}, username: {self.username}>"

    @property
    def password(self) -> None:
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
