"""Shoot factory"""

import factory
from faker import Factory as FakerFactory

from src.models import Shoot
from tests.factories.base import BaseFactory

faker = FakerFactory.create()


class ShootFactory(BaseFactory):
    """Shoot factory"""
    name = factory.LazyAttribute(lambda x: faker.sentence(nb_words=3))
    description = factory.LazyAttribute(lambda x: faker.text())
    price = factory.Iterator([20000, 30000, 40000, 50000, 60000])
    duration = factory.Iterator([20, 30, 40, 50, 60, 10])

    class Meta:
        """Meta class"""

        model = Shoot
