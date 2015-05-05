#    Copyright 2015 Dat Do
#    
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#    
#        http://www.apache.org/licenses/LICENSE-2.0
#    
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


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
    beef = db.Column(db.Boolean, nullable=True)
    dairy = db.Column(db.Boolean, nullable=True)
    egg = db.Column(db.Boolean, nullable=True)
    fish = db.Column(db.Boolean, nullable=True)
    gluten = db.Column(db.Boolean, nullable=True)
    meat = db.Column(db.Boolean, nullable=True)
    nut = db.Column(db.Boolean, nullable=True)
    pork = db.Column(db.Boolean, nullable=True)
    poultry = db.Column(db.Boolean, nullable=True)
    shellfish = db.Column(db.Boolean, nullable=True)
    soy = db.Column(db.Boolean, nullable=True)
    wheat = db.Column(db.Boolean, nullable=True)
    notes = db.Column(db.String, nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    def __init__(self, name, price, image, beef, dairy, egg, fish, gluten, meat, 
                 nut, pork, poultry, shellfish, soy, wheat, notes, restaurant_id):
        self.name = name
        self.date = datetime.datetime.utcnow()
        self.price = price
        self.image = image
        self.beef = beef
        self.dairy = dairy
        self.egg = egg
        self.fish = fish
        self.gluten = gluten
        self.meat = meat
        self.nut = nut
        self.pork = pork
        self.poultry = poultry
        self.shellfish = shellfish
        self.soy = soy
        self.wheat = wheat
        self.notes = notes
        self.restaurant_id = restaurant_id

    def __repr__(self):
        return '<Dish {}>'.format(self.name)


# FIXME: How should this be adapted to integrate with Google and Facebook user services
class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.Date, default=datetime.datetime.utcnow())
    image = db.Column(db.String, nullable=True)
    score = db.Column(db.Integer, default=0)
    dishes = db.relationship('Dish', backref='user')
   
    def __init__(self, name, image):
        self.name = name
        self.date = datetime.datetime.utcnow()
        self.image = image
        self.score = 0

    def __repr__(self):
        return '<User {}>'.format(self.name)
