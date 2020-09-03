"""Module for Pytest Configuration"""

from os import getenv, environ
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

from database.config import Base
from main import create_app

testing_env = 'testing'
environ['FLASK_ENV'] = testing_env
env = getenv('FLASK_ENV')
load_dotenv()

TEST_DATABASE_URL = getenv('TEST_DATABASE_URL')
engine = create_engine(TEST_DATABASE_URL, echo=True)
Session = scoped_session(sessionmaker(bind=engine))


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
    
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)
