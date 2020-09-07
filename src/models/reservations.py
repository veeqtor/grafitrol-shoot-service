"""Reservations model"""
import enum
from datetime import timedelta

from sqlalchemy import (Column, String, Integer, ForeignKey, Text, DateTime)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from src.models.base import BaseModel
from utils.datetime_helpers import localize_datetime


class StatusChoices(enum.Enum):
    """
	Reservation status enums
	"""
    Pending = '0'
    Completed = '1'
    Done = '2'


class Reservation(BaseModel):
    """Reservation Model"""

    __tablename__ = 'reservations'

    UNIQUE_VIOLATION_MSG = 'Reservation already Exists'

    STATUS_ENUM = ENUM(
        StatusChoices,
        name='reservation_status',
    )

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(100), nullable=False, unique=True)
    additional_info = Column(Text, nullable=True)

    status = Column(STATUS_ENUM, nullable=False, default='0')
    reservation_datetime = Column(DateTime(timezone=True), nullable=False)
    duration = Column(Integer, nullable=False, default=30)

    coordinator_id = Column(String(30), ForeignKey('coordinators.id'))
    coordinator = relationship("Coordinator", back_populates="reservations")

    shoot_id = Column(String(30), ForeignKey('shoots.id'))
    shoot = relationship("Shoot", back_populates="reservations")

    @hybrid_property
    def reservation_end_datetime(self):
        """The end datetime for the reservation"""
        return localize_datetime(self.reservation_datetime +
                                 timedelta(minutes=self.duration))

    def __repr__(self):
        """ Informative name for model """

        return f"<Reservation {self.status} - {self.reservation_datetime} - " \
               f"{self.duration}>"
