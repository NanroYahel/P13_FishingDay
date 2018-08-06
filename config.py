# Configurations varibales
import os

class Config(object):
	"""Contain all the KEY needed by the application"""
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
	OWM_API_KEY = os.environ.get('OWM_API_KEY')

