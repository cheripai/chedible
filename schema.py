import datetime
from FIXME import db


class Restaurant(db.model):
    
    __tablename__ = "restaurant"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    dishes = db.relationship('Dish', backref='restaurant')
    # should there be location? and how will we reference multiple locations


class Dish(db.model):
    
    __tablename__ = "dish"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, default=datetime.datetime.utcnow())
    price = db.Column(db.Float, precision=2, nullable=True)
    image = db.Column(db.String, nullable=True)
    dairy = db.Column(db.Boolean, nullable=True)
    egg = db.Column(db.Boolean, nullable=True)
    fish = db.Column(db.Boolean, nullable=True)
    gluten = db.Column(db.Boolean, nullable=True)
    meat = db.Column(db.Boolean, nullable=True)
    nut = db.Column(db.Boolean, nullable=True)
    shellfish = db.Column(db.Boolean, nullable=True)
    soy = db.Column(db.Boolean, nullable=True)
    wheat = db.Column(db.Boolean, nullable=True)
    notes = db.Column(db.String, nullable=True)
