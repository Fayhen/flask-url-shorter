import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clicks = db.Column(db.Integer, nullable=False, default=0)
    short_url = db.Column(db.String, unique=True, nullable=False)
    long_url = db.Column(db.String, nullable=False)


# Setup database from terminal
@click.command('setup-db')
@with_appcontext
def setup_database():
    """
    Creates new tables and the database file.
    Warning: clears all existing data, if any.
    """
    db.create_all()
    click.echo('Database created.')


# Teardown database from terminal
@click.command('destroy-db')
@with_appcontext
def destroy_database():
    db.drop_all()
    click.echo('Database destroyed.')
