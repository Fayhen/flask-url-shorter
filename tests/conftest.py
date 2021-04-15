import pytest
from flask_sqlalchemy import SQLAlchemy

import config
from api import create_app
# from api.database import setup_db, populate_db, destroy_db


@pytest.fixture
def app():
    # test_engine = create_engine(config.TEST_DATABASE_URI, convert_unicode=True)
    # test_session = scoped_session(sessionmaker(autocommit=False,
    #                                            autoflush=False,
    #                                            bind=test_engine))

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': config.TEST_DATABASE_URI,
        'SQLALCHEMY_TRACK_MODIFICATIONS': config.SQLALCHEMY_TRACK_MODIFICATIONS
    })

    # with app.app_context():
    #     setup_db(engine_env=test_engine)
    #     populate_db(session=test_session)

    yield app


@pytest.fixture
def db(app):
    runner = app.test_cli_runner()
    runner.invoke(args=['setup-db'])

    with app.app_context():
        db = SQLAlchemy()
        db.init_app(app)

        yield db

    runner.invoke(args=['destroy-db'])


@pytest.fixture
def client(app):
    runner = app.test_cli_runner()
    runner.invoke(args=['setup-db'])
    runner.invoke(args=['populate-db'])

    yield app.test_client()

    runner. invoke(args=['destroy-db'])


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
