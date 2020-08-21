from os import path

from flask_migrate import Migrate, upgrade

from my_app import App, db as database
from .support.fixtures.models import *


@pytest.fixture(scope='session')
def app():
    """Session-wide test Flask application"""

    config_override = {
        'TESTING': True
    }

    app = App(config=config_override)
    configure_test_db(app)

    with app.app_context():
        yield app


def configure_test_db(app: App):
    """Set local sqlite test db"""

    db_path = path.dirname(path.abspath(__file__))
    test_db = 'sqlite:///{}/test.db'.format(db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = test_db


@pytest.fixture(scope='session')
def db(app: App):
    """Session-wide test database"""

    database.app = app
    cleanup_db(database)

    # bring database schema up to date
    Migrate(app, database)

    with app.app_context():
        upgrade()

    yield database
    cleanup_db(database)


def cleanup_db(db):
    """Clean up the given database"""

    db.reflect()
    db.drop_all()


@pytest.fixture(scope='function')
def session(db):
    """Create a new database session for a test"""

    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()


@pytest.fixture(scope='function')
def client(app, session):
    """Function-wide test client"""

    yield app.test_client()
