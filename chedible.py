from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


# config
app = Flask(__name__)
app.config.from_object('_config')
db = SQLAlchemy(app)

from schema import Restaurant, Dish
