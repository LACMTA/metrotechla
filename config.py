class Config(object):
	SECRET_KEY = 'ssshhhhh'
	DEBUG = False
	TESTING = False
	# MAIL_SERVER = 'smtp.example.com'
	# MAIL_PORT = 465
	# MAIL_USE_SSL = True
	# MAIL_USERNAME = 'username'
	# MAIL_PASSWORD = 'password'
	# DATABASE_URI = 'sqlite://:memory:'
	# FLASK-SECURITY
	SECURITY_REGISTERABLE = True
	SECURITY_REGISTER_URL = '/register'

class ProductionConfig(Config):
	SECRET_KEY = 'ssshhhhh'
	# DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
	SECRET_KEY = 'ssshhhhh'
	DEBUG = True

class TestingConfig(Config):
	SECRET_KEY = 'ssshhhhh'
	TESTING = True
