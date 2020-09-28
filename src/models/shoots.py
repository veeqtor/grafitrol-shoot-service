"""Shoots model"""

from sqlalchemy import Column, String, Text, Float, Integer
from sqlalchemy.orm import relationship

from src.models.reservations import Reservation
from src.models.base import BaseModel


class Shoot(BaseModel):
    """Shoots Model"""

    __tablename__ = 'shoots'

    UNIQUE_VIOLATION_MSG = 'Shoot already Exists'

    name = Column(String(50), unique=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    duration = Column(Integer, default=30, nullable=False)
    reservations = relationship("Reservation",
                                order_by=Reservation.id,
                                back_populates="shoot")

    def __repr__(self):
        """ Informative name for model """

        return f"<Studio Shoots {self.name}>"
