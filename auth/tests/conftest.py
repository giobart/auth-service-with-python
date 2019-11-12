import datetime
import os
import tempfile

from flask import jsonify

from auth.app import create_app
from auth.database import User, db

import pytest


@pytest.fixture
def app():
    '''
    Builds and configures a new app instance for each test, using the test
    flag and a temporary fresh database.

    Automatically manages the temporary files.

    Can be overridden locally to pass different flags to the app instance,
    see test_unitStories for reference.
    '''

    db_fd, db_path = tempfile.mkstemp()
    db_url = 'sqlite:///' + db_path
    app = create_app(database=db_url)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


class ClientFactory:

    def __init__(self, app):
        self._app = app

    def get(self):
        return self._app.test_client()


@pytest.fixture
def client_factory(app):
    return ClientFactory(app)


@pytest.fixture
def client(app, client_factory):
    '''
    Builds a new test client instance.
    '''
    return client_factory.get()


def _init_database(db):
    '''
    Initializes the database for testing.
    '''
    example1 = User()
    example1.username = 'test1'
    example1.firstname = 'First1'
    example1.lastname = 'Last1'
    example1.email = 'test1@example.com'
    example1.dateofbirth = datetime.datetime(2020, 10, 5)
    example1.is_admin = False
    example1.set_password('test1123')
    db.session.add(example1)

    db.session.commit()


@pytest.fixture
def database(app):
    '''
    Provides a reference to the temporary database in the app context. Use
    this instance instead of importing db from monolith.db.
    '''
    with app.app_context():
        db.create_all()

        _init_database(db)
        yield db

        db.drop_all()
        db.session.commit()

