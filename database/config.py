"""Database Definition"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.getenv('DATABASE_URL')
TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL')

engine = create_engine(TEST_DATABASE_URL, echo=True)
if os.getenv('FLASK_ENV') != 'testing':
    engine = create_engine(DATABASE_URL, echo=True)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """Initial DB"""
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import src.models
    Base.metadata.create_all(bind=engine)
