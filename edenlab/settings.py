# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config(object):
    """Base configuration."""

    SECRET_KEY = os.environ.get('REPOSITORY-API_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAGINATION_ENABLED = True
    DEFAULT_RESULTS_PER_PAGE = 15


class ProdConfig(Config):
    """Production configuration."""

    ENV = 'prod'
    DEBUG = False
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    DB_SERVICE = os.environ.get('DB_SERVICE')
    DB_PORT = os.environ.get('DB_PORT')
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME)
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'sqlite.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    DEBUG_TB_ENABLED = True
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
