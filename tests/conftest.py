"""Module for Pytest Configuration"""

from os import getenv, environ
import pytest
from dotenv import load_dotenv

from main import create_app

testing_env = 'testing'
environ['FLASK_ENV'] = testing_env
env = getenv('FLASK_ENV')
load_dotenv()


@pytest.fixture(scope='session')
def flask_app():
    """
	Create a flask application instance for Pytest.
	Returns:
		Object: Flask application object
	"""

    # create an application instance
    _app = create_app(env)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    # yield the application context for making requests
    yield _app

    ctx.pop()


@pytest.fixture
def client(flask_app):
    """Setup client for making http requests, this will be run on every test
	function.
	Args:
		flask_app (func): Flask application instance
	Returns:
		Object: flask application client instance
	"""

    # initialize the flask test_client from the flask application instance
    client = flask_app.test_client()

    yield client


@pytest.fixture(scope="function")
def db_session():
    """Database session"""
    # importing this here so that the env is set properly before creating
    # the db engine
    from database.config import Base, db_session as Session, engine

    Base.metadata.create_all(engine)
    session = Session()
    Base.query = Session.query_property()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def new_coordinators(db_session):
    """Create new coordinators"""
    from tests.factories import CoordinatorFactory
    return CoordinatorFactory.create_batch(size=10)


@pytest.fixture(scope="function")
def new_shoots(db_session):
    """Create new shoots"""
    from tests.factories import ShootFactory
    return ShootFactory.create_batch(size=10)
