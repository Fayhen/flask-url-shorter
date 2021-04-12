import csv
import click
import config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


@click.command('setup-db')
def setup_db(engine_env=engine):
    """
    Setups database from scratch. Models must be imported to
    create their corresponding tables.
    """
    import api.models
    Base.metadata.create_all(bind=engine_env)
    click.echo('Database created.')


@click.command('destroy-db')
def destroy_db(engine_env=engine):
    """
    Erases the database. All data and tables are removed. This
    operation is irreversible.
    """
    Base.metadata.drop_all(bind=engine_env)
    click.echo('Database destroyed.')


@click.command('populate-db')
def populate_db(session=db_session):
    """
    Populate database with data from a CSV file.
    """
    from api.models import Url
    from api.methods import generate_hash

    with open('api/assets/sites_list.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            # Create and save new URL instance to generate its ID
            new_url = Url(long_url=row[0])
            session.add(new_url)
            session.commit()

            # Generate and save a short URL hash using the ID
            new_hash = generate_hash(new_url.id)
            new_url.hash = new_hash
            session.add(new_url)
            session.commit()

    click.echo('Data added.')
