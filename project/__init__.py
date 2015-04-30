from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


# config
app = Flask(__name__)
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)

from project.schema import Restaurant, Dish
from project.chedible import *
