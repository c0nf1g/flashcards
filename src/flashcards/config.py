import os


class Config:
    """Base configuration"""

    SECRET_KEY = os.getenv("SECRET_KEY", "my code")
    TOKEN_EXPIRE_HOURS = 0
    TOKEN_EXPIRE_MINUTES = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URI")


class DevelopmentConfig(Config):
    """Development configuration"""

    TOKEN_EXPIRE_MINUTES = 50
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI")


class ProductionConfig(Config):
    """Production Configuration"""

    TOKEN_EXPIRE_HOURS = 1
    BCRYPT_LOG_ROUNDS = 12
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URI")
    PRESERVE_CONTEXT_ON_EXCEPTION = True


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)


def get_config(config_name):
    return ENV_CONFIG_DICT.get(config_name, ProductionConfig)
