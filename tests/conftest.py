# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
from webtest import TestApp

from edenlab.app import create_app
from edenlab.database import db as _db
from edenlab.settings import TestConfig


from tests.factories import RepositoryFactory


@pytest.fixture
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.fixture
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def repository(db):
    """A repository for tests"""
    repo = RepositoryFactory(full_name='python', language='Python')
    db.session.commit()
    return repo


@pytest.fixture
def repositories(db):
    """List of repositories for tests"""
    repos = list()
    repos.append(RepositoryFactory(full_name='python', language='Python'))
    repos.append(RepositoryFactory(full_name='ruby', language='Ruby'))
    repos.append(RepositoryFactory(full_name='java', language='Java'))
    db.session.commit()
    return repos
