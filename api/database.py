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
def setup_db():
    import api.models
    Base.metadata.create_all(bind=engine)
    click.echo('Database created.')


@click.command('destroy-db')
def destroy_db():
    Base.metadata.drop_all(bind=engine)
    click.echo('Database destroyed.')


@click.command('populate')
def populate():
    from api.models import Url
    an_url = Url(long_url='exampleurl.com', short_url='31sG')
    db_session.add(an_url)
    db_session.commit()
    click.echo('Dummy data added.')
