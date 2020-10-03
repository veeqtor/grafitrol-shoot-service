"""Shoot factory"""
import random
from datetime import datetime, timedelta

import factory
from faker import Factory as FakerFactory

from main import utc
from src.models import Reservation
from src.models.reservations import ReservationStatusChoices
from tests.factories import CoordinatorFactory, ShootFactory
from tests.factories.base import BaseFactory

faker = FakerFactory.create()


class ReservationsFactory(BaseFactory):
    """Reservation factory"""

    first_name = factory.LazyAttribute(lambda x: faker.first_name())
    last_name = factory.LazyAttribute(lambda x: faker.last_name())
    email = factory.LazyAttribute(lambda x: faker.email())
    phone = factory.LazyAttribute(lambda x: faker.phone_number())
    reservation_datetime = factory.LazyAttribute(lambda x: datetime.now(
        tz=utc).replace(minute=random.randrange(0, 60, 15),
                        hour=random.randrange(8, 16, 1),
                        second=0) + timedelta(days=random.randrange(1, 10, 1)))
    duration = factory.Iterator([60, 90, 120])
    status = factory.Iterator(ReservationStatusChoices)
    coordinator = factory.SubFactory(CoordinatorFactory)
    shoot = factory.SubFactory(ShootFactory)

    class Meta:
        """Meta class"""
        model = Reservation
