import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'This is your secret_key'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	#FLASKY_MAIL_SUBJECT_PREFIX = '[SummerBlog]'
	#FLASKY_MAIL_SENDER = 'SummerBlog Admin <admin@summerblog.com>'
	#FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = ''
	#MAIL_PORT = 
	#MAIL_USE_TLS = 
	#MAIL_USERNAME = 
	#MAIL_PASSWORD = 
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class ProductConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
	'development':DevelopmentConfig,
	'testing':TestingConfig,
	'production':ProductConfig,
	'default':DevelopmentConfig
}