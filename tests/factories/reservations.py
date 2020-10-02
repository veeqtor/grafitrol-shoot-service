"""Shoot factory"""
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

    first_name = factory.LazyAttribute(lambda x: faker.name())
    last_name = factory.LazyAttribute(lambda x: faker.name())
    email = factory.LazyAttribute(lambda x: faker.email())
    phone = factory.LazyAttribute(lambda x: faker.phone_number())
    reservation_datetime = factory.LazyAttribute(
        lambda x: datetime.now(tz=utc) + timedelta(days=2))
    duration = factory.Iterator([60, 90, 120])
    status = factory.Iterator(ReservationStatusChoices)
    coordinator = factory.SubFactory(CoordinatorFactory)
    shoot = factory.SubFactory(ShootFactory)

    class Meta:
        """Meta class"""
        model = Reservation
