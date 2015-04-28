import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'data.db'
DATABASE_PATH = os.path.join(basedir, DATABASE)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
