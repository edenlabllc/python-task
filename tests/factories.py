# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory


from edenlab.database import db
from edenlab.repository.models import Repository


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class RepositoryFactory(BaseFactory):
    full_name = Sequence(lambda n: '{0}-test'.format(n))
    language = Sequence(lambda n: '{0}-lang'.format(n))


    class Meta:
        """Factory configuration."""

        model = Repository
