# Configurations varibales
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	"""Contain all the KEY needed by the application"""
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
	OWM_API_KEY = os.environ.get('OWM_API_KEY')
	WT_API_KEY = os.environ.get('WT_API_KEY')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False



