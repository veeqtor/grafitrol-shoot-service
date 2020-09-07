"""Coordinators model"""

from sqlalchemy import Column, String, Time, Integer, Boolean
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship

from src.helpers.shoots_slots import (get_datetime_and_capacity,
                                      generate_slots, filter_slots, INTERVAL)
from src.models.reservations import Reservation
from src.models.base import BaseModel
from utils.datetime_helpers import date_validator


class Coordinator(BaseModel):
    """Coordinator Model"""

    __tablename__ = 'coordinators'

    UNIQUE_VIOLATION_MSG = 'Coordinator already Exists'

    start_of_day = Column(Time, nullable=False)
    end_of_day = Column(Time, nullable=False)
    break_start_time = Column(Time, nullable=False)
    break_duration = Column(Integer, nullable=False, default=60)
    is_available = Column(Boolean, nullable=False, default=True)
    user = Column(String(100), nullable=False, unique=True)
    reservations = relationship("Reservation",
                                order_by=Reservation.id,
                                back_populates="coordinator")

    @hybrid_property
    def slots(self):
        """Get slots for this coordinator"""
        return self.get_slots_by_date()

    @hybrid_method
    def get_slots_by_date(self, day=None):
        """
		Get all slots for the coordinator
		"""
        validated_date = None
        if day:
            validated_date = date_validator(day)

        capacity, start, end = get_datetime_and_capacity(self.start_of_day,
                                                         self.end_of_day,
                                                         INTERVAL,
                                                         day=validated_date)
        slots = generate_slots(start, capacity)
        filtered_slots = filter_slots(self.reservations, self.break_duration,
                                      self.break_start_time, validated_date,
                                      slots)
        return [slot for slot in filtered_slots]

    def __repr__(self):
        """ Informative name for model """

        return f"<Coordinator {self.user}>"
