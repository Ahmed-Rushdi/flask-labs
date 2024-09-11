from app import db
from sqlalchemy import Column, Integer, String, BLOB
from sqlalchemy.orm import relationship, Mapped
import bcrypt


class Book(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(80), unique=True, nullable=False)
    cover = Column(BLOB, nullable=True)

    def __repr__(self) -> str:
        return f"<Book {self.id}, title: {self.title}>"


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(256), unique=False, nullable=False)
    avatar = Column(BLOB, nullable=True)

    books: Mapped[list[Book]] = relationship()

    def __repr__(self) -> str:
        return f"<User {self.id}, username: {self.username}>"

    @property
    def password(self) -> None:
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password: str) -> None:
        self.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
