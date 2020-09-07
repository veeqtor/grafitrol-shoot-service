"""Base factory"""
from datetime import datetime

import factory
from faker import Factory as FakerFactory

from database.config import db_session as dbSession
from utils.id_generator import IDGenerator

faker = FakerFactory.create()


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Base factory"""

    __abstract__ = True

    id = factory.LazyFunction(IDGenerator.generate_id)
    version = factory.Sequence(lambda n: n)
    created_at = factory.LazyFunction(datetime.now)

    class Meta:
        """Meta class"""

        sqlalchemy_session = dbSession
        sqlalchemy_session_persistence = 'commit'
