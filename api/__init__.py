import os
import config
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Globally accessible libraries
db = SQLAlchemy()


# Refactor to include al database connections in the configuration being passed to the app factory
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=config.SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=config.SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=config.SQLALCHEMY_TRACK_MODIFICATIONS
    )

    # Override default with test configuration, if any
    if test_config is not None:
        app.config.from_mapping(test_config)

    # Ensure instance folder
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        print('Error: Unable to create app instance directory.')

    db.init_app(app)

    with app.app_context():
        # Database
        # engine = create_engine(config.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
        # db_session = scoped_session(sessionmaker(autocommit=False,
        #                                          autoflush=False,
        #                                          bind=engine))
        # engine, session = init_db(app)

        from api.database import setup_db, destroy_db, populate_db
        app.cli.add_command(setup_db)
        app.cli.add_command(destroy_db)
        app.cli.add_command(populate_db)

        # Blueprints
        from api.routes import api
        app.register_blueprint(api)

    # @app.teardown_appcontext
    # def shutdown_session(exception=None):
    #     db_session.remove()

    # print(app.config)
    print("Ran the app factory.")

    return app
