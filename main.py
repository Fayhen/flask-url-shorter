import os
import config
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy


# db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=config.SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=config.SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=config.SQLALCHEMY_TRACK_MODIFICATIONS
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from api.database import db, setup_database, destroy_database, populate
    db.init_app(app)
    app.cli.add_command(setup_database)
    app.cli.add_command(destroy_database)
    app.cli.add_command(populate)

    # Ensure instance folder
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        print('Error: Unable to create app instance directory.')

    from api.routes import api
    app.register_blueprint(api)

    # print(app.config)
    print("Ran the app factory.")

    return app
