"""Coordinator factory"""
from datetime import time

import factory
from faker import Factory as FakerFactory

from src.models import Coordinator
from tests.factories.base import BaseFactory

faker = FakerFactory.create()


class CoordinatorFactory(BaseFactory):
    """Coordinator factory"""

    start_of_day = factory.LazyAttribute(lambda x: time(8, 0, 0))
    end_of_day = factory.LazyAttribute(lambda x: time(18, 0, 0))
    break_start_time = factory.LazyAttribute(lambda x: time(12, 0, 0))
    break_duration = factory.Iterator([20, 30, 40, 50, 60, 10])
    user = factory.LazyAttribute(lambda x: faker.name())
    reservations = factory.RelatedFactory(
        'tests.factories.reservations.ReservationsFactory',
        factory_related_name='coordinator',
    )

    class Meta:
        """Meta class"""
        model = Coordinator
