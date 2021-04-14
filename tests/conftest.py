import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import config
from api import create_app
from api.database import setup_db, populate_db, destroy_db


# Refactor to include al database connections in the configuration being passed to the app factory
@pytest.fixture
def db():
    test_engine = create_engine(config.TEST_DATABASE_URI, convert_unicode=True)
    test_session = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=test_engine))
    _db = {
        'engine': test_engine,
        'session': test_session
    }

    # print(setup_db.__init__)
    setup_db(test_engine)
    populate_db(test_session)

    yield _db

    # Code written after an 'yield' statement is executed at context teardown
    destroy_db(test_session)


@pytest.fixture
def app():
    # test_engine = create_engine(config.TEST_DATABASE_URI, convert_unicode=True)
    # test_session = scoped_session(sessionmaker(autocommit=False,
    #                                            autoflush=False,
    #                                            bind=test_engine))

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS': config.SQLALCHEMY_TRACK_MODIFICATIONS
    })

    # with app.app_context():
    #     setup_db(engine_env=test_engine)
    #     populate_db(session=test_session)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
