from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

    # print(f"{app.config=}")
    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/hello")
    def hello():
        return "Hello World!"

    return app
