"""User model"""

from sqlalchemy import Column, String
from src.models.base import BaseModel


class User(BaseModel):
	"""User Model"""
	
	__tablename__ = 'users'
	
	UNIQUE_VIOLATION_MSG = 'User already Exists'
	
	name = Column(String(50), unique=True)
	email = Column(String(120), unique=True)
	
	def __repr__(self):
		return '<User %r>' % (self.name)
