import os
# import click
import config
from flask import Flask, request
# from flask.cli import with_appcontext
# from flask_sqlalchemy import SQLAlchemy


# db = SQLAlchemy()


# # Setup database from terminal
# @click.command('setup-db')
# @with_appcontext
# def setup_database():
#     """
#     Creates new tables and the database file.
#     Warning: clears all existing data, if any.
#     """
#     # db.create_all()
#     click.echo('Database created.')
#
#
# # Teardown database from terminal
# @click.command('destroy-db')
# @with_appcontext
# def destroy_database():
#     # db.drop_all()
#     click.echo('Database destroyed.')


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=config.SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=config.SQLALCHEMY_DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=config.SQLALCHEMY_TRACK_MODIFICATIONS
    )
    # app.cli.add_command(setup_database)
    # app.cli.add_command(destroy_database)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # db.init_app(app)

    # Ensure instance folder
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        print('Error: Unable to create app instance directory.')

    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'
    #
    # @app.route('/short-url', methods=['POST'])
    # def short_url():
    #     print(request.data)
    #     return 'short url'
    #
    # @app.route('/redirect-url', methods=['GET'])
    # def redirect_url():
    #     print(request)
    #     return 'redirect url'

    from api.routes import api
    app.register_blueprint(api)

    # print(app.config)
    print("Ran the app factory.")

    return app
