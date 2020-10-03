"""Base model class"""
from datetime import datetime

from psycopg2 import errors
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column, Integer, DateTime, String, exists

from database.config import Base, db_session
from src.helpers.messages import ERROR_MSG
from utils.exceptions import DataConflictException, ResponseException
from utils.id_generator import IDGenerator


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

    def delete(self):
        """Delete an entry"""

        db_session.delete(self)
        db_session.commit()

    @classmethod
    def get(cls, id):
        """
		Returns an entry by id
		"""
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_or_404(cls, id):
        """
	    Return an entry or throws a 404 if not found
	    """
        entry = cls.get(id)
        msg = ERROR_MSG['SYS_009'].format(cls.__name__)
        if not entry:
            raise ResponseException(msg, 404)
        return entry

    @classmethod
    def exists(cls, value, column='id'):
        """Checks if an object exits in the database
		Args:
			value (str): The value to verify
			column (str): The column to check. Defaults to 'id'
		Returns:
			bool: True if the value exists, False otherwise
		"""
        attr = getattr(cls, column)
        return db_session.query(exists().where(attr == value)).scalar()


class BaseAuditableModel(object):
    """
	Auditable Base Model
	"""

    __abstract__ = True

    version = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.now)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now)


class BaseModel(Base, BaseAuditableModel, ModelOperation):
    """
	Base Model
	"""

    __abstract__ = True

    id = Column(String(30), primary_key=True, default=IDGenerator.generate_id)
