"""Configurations varibales"""
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Contain all the KEY needed by the application"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    OWM_API_KEY = os.environ.get('OWM_API_KEY')
    WT_API_KEY = os.environ.get('WT_API_KEY')
    MAPS_API_KEY = os.environ.get('MAPS_API_KEY')
    #DATABASE
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASEDIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ConfigTest(object):
    """Contain the configuration for the tests"""
    SECRET_KEY = 'fake_secret_key'
    OWM_API_KEY = 'fake_owm_api_key'
    WT_API_KEY = 'fake_wt_api_key'
    MAPS_API_KEY = 'fake_maps_api_key'
    DEBUG = True
    # DATABASE
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app_test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Reduce Bcrypt algorithm for performance
    BCRYPT_LOG_ROUNDS = 4
    TESTING = True
    # Disable CSRF tokens for performance
    WTF_CSRF_ENABLED = False
