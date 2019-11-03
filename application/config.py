import os


class Config(object):

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '12345'

    pw                        = os.environ.get('DB_PASSWORD', 'password')
    user                      = os.environ.get('DB_USER', 'postgres')
    url                       = os.environ.get('DB_HOST', 'localhost')
    db                        = os.environ.get('DB_NAME', "postgres")

    # postgres
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{pw}@{url}/{db}'

    S3_BUCKET                 = os.environ.get("S3_BUCKET_NAME")
    S3_KEY                    = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET                 = os.environ.get("S3_SECRET_ACCESS_KEY")
    S3_LOCATION               = f'http://{S3_BUCKET}.s3.amazonaws.com/'

    # Flask-User configuration
    # USER_APP_NAME = "Flasky To-Do App"      # Shown in and email templates and page footers
    # USER_ENABLE_EMAIL = False      # Disable email authentication
    # USER_ENABLE_USERNAME = True    # Enable username authentication
    # USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True