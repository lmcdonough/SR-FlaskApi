import os

SECRET_KEY = 'you-will-never-guess'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql://levi:python@localhost/simpledb'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
