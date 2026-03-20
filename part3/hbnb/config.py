import os


class Config:
    """Base configuation class"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    """Developpement environnement configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///developpement.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
