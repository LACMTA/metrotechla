class Config(object):
	SECRET_KEY = 'ssshhhhh'
	DEBUG = False
	TESTING = False
	MAIL_SERVER = 'smtp.sendgrid.net'
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USERNAME = 'goodwindo'
	MAIL_PASSWORD = '9Hi5AgXK96'
	# DATABASE_URI = 'sqlite://:memory:'
	# FLASK-SECURITY
	SECURITY_REGISTERABLE = True
	SECURITY_REGISTER_URL = '/register'
	SECURITY_CONFIRMABLE = False
	SECURITY_RECOVERABLE = False
	SECURITY_SEND_REGISTER_EMAIL = False
	SECURITY_DEFAULT_REMEMBER_ME = True

class ProductionConfig(Config):
	SECRET_KEY = 'ssshhhhh'
	# DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
	SECRET_KEY = 'ssshhhhh'
	DEBUG = True

class TestingConfig(Config):
	SECRET_KEY = 'ssshhhhh'
	TESTING = True
