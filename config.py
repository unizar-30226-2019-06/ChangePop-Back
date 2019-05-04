import os
import django_heroku
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object): # pragma: no cover
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class ProductionConfig(Config): # pragma: no cover
    DEBUG = False


class StagingConfig(Config): # pragma: no cover
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config): # pragma: no cover
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config): # pragma: no cover
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

try: # pragma: no cover
    # Activate Django-Heroku.
    django_heroku.settings(locals())
except KeyError: # pragma: no cover
    print("No running in heroku")
