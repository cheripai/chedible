import datetime
from project import db


class Restaurant(db.Model):
    
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    dishes = db.relationship('Dish', backref='restaurant')
    # should there be location? and how will we reference multiple locations

    def __init__(self, name, category, image):
        self.name = name
        self.category = category
        self.image = image

    def __repr__(self):
        return '<Restaurant {}'.format(self.name)


class Dish(db.Model):
    
    __tablename__ = "dishes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, default=datetime.datetime.utcnow())
    price = db.Column(db.Float(Precision=2), nullable=True)
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
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    def __init__(self, name, date, price, image, dairy, egg, fish, gluten, 
                 meat, nut, shellfish, soy, wheat, notes, restaurant_id):
        self.name = name
        self.date = date
        self.price = price
        self.image = image
        self.dairy = dairy
        self.egg = egg
        self.fish = fish
        self.gluten = gluten
        self.meat = meat
        self.nut = nut
        self.shellfish = shellfish
        self.soy = soy
        self.wheat = wheat
        self.notes = notes
        self.restaurant_id = restaurant_id

    def __repr__(self):
        return '<Dish {}>'.format(self.name)
