"""Base model class"""

from psycopg2 import errors
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column, Integer

from database.config import Base, db_session
from utils.exceptions import DataConflictException


class ModelOperation(object):
    """Model operation"""
    
    __abstract__ = True

    UNIQUE_VIOLATION_MSG = ''

    def save(self):
        """Save to the database."""
        
        db_session.add(self)
        try:
            db_session.commit()
        except IntegrityError as e:
            if isinstance(e.orig, errors.UniqueViolation):
                raise DataConflictException(message=self.UNIQUE_VIOLATION_MSG)
        return self

    def update(self, **kwargs):
        """Update entries.
        Args:
            **kwargs: kwargs to update
        Returns:
            object: Model Instance
        """
        for field, value in kwargs.items():
            setattr(self, field, value)
        db_session.commit()

        return self


class BaseModel(Base, ModelOperation):
    """User Model"""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
