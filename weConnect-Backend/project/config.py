# project/config.py

import os

class BaseConfig:
	"""Base Configurations"""
	DEBUG = False
	TESTING = False
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.environ.get('SECRET_KEY')
	BCRYPT_LOG_ROUNDS = 13
	TOKEN_EXPIRATION_DAYS = 30
	TOKEN_EXPIRATION_SECONDS = 0	

class DevelopmentConfig:
	"""Development Configurations"""
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'postgres://postgres:peter926@localhost:5432/users_dev'
	BCRYPT_LOG_ROUNDS = 4
	SECRET_KEY = os.environ.get('SECRET_KEY')	
  

class ProductionConfig:
	"""Production Configurations"""
	DEBUG = False
	TESTING = False
	#SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')    

class TestingConfig:
	"""Testing Configurations"""
	DEBUG = True
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'postgres://postgres:peter926@localhost:5432/users_test'
	BCRYPT_LOG_ROUNDS = 4
	SECRET_KEY = os.environ.get('SECRET_KEY')	
    