# import tempfile
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import config
from api import create_app
from api.database import setup_db, populate_db


@pytest.fixture
def app():
    # db_fd, db_path = tempfile.mkstemp()
    test_engine = create_engine(config.TEST_DATABASE_URI, convert_unicode=True)
    test_session = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=test_engine))

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS': config.SQLALCHEMY_TRACK_MODIFICATIONS
    })

    with app.app_context():
        setup_db(engine_env=test_engine)
        populate_db(session=test_session)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
