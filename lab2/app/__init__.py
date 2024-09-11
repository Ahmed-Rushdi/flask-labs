from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app.utils import bytes_to_base64

db = SQLAlchemy()


def create_app(**custom_config):
    app = Flask(__name__)

    config = {
        "SECRET_KEY": "dev",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///db.sqlite",
        # "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }
    config.update(custom_config)
    app.config.from_mapping(config)
    app.jinja_env.filters["bytes_to_base64"] = bytes_to_base64
    # print(f"{app.config=}")
    db.init_app(app)

    from app import models

    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return render_template("layout.html")

    from app.blueprints import auth, books

    app.register_blueprint(auth.bp)
    app.register_blueprint(books.bp)

    return app
