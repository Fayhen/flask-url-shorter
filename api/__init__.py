import os
import config
from flask import Flask


# Refactor to include al database connections in the configuration being passed to the app factory
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=config.SECRET_KEY,
        SQLALCHEMY_TRACK_MODIFICATIONS=config.SQLALCHEMY_TRACK_MODIFICATIONS
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure instance folder
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        print('Error: Unable to create app instance directory.')

    # Database
    from api.database import db_session, setup_db, destroy_db, populate_db
    app.cli.add_command(setup_db)
    app.cli.add_command(destroy_db)
    app.cli.add_command(populate_db)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # Blueprints
    from api.routes import api
    app.register_blueprint(api)

    # print(app.config)
    print("Ran the app factory.")

    return app
