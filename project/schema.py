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


from datetime import datetime
from project import db
from flask.ext.sqlalchemy import BaseQuery
from locale import currency
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable
from time import time

make_searchable()

class RestaurantQuery(BaseQuery, SearchQueryMixin):
    pass


class Restaurant(db.Model):
    query_class = RestaurantQuery
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    dishes = db.relationship('Dish', backref='restaurant')
    tags = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_edited = db.Column(db.Integer, nullable=False)
    search_vector = db.Column(TSVectorType('name', 'category', 'tags'))
    # FIXME: should there be location? and how will we reference multiple locations

    def __init__(self, name, category, image, tags, user_id):
        self.name = name
        self.date = datetime.utcnow()
        self.category = category
        self.image = image
        self.tags = tags
        self.user_id = user_id
        self.last_edited = int(time())

    def __repr__(self):
        return '<Restaurant {}>'.format(self.name)


class DishQuery(BaseQuery, SearchQueryMixin):
    pass


class Dish(db.Model):
    query_class = DishQuery   
    __tablename__ = "dishes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    price = db.Column(db.String, nullable=True)
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
    score = db.Column(db.Integer)
    notes = db.Column(db.String, nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_edited = db.Column(db.Integer, nullable=False)
    search_vector = db.Column(TSVectorType('name'))

    def __init__(self, name, price, image, beef, dairy, egg, fish, gluten, meat, 
                 nut, pork, poultry, shellfish, soy, wheat, notes, restaurant_id, user_id):
        self.name = name
        self.date = datetime.utcnow()
        if price:
            self.price = currency(float(price), grouping=True)
        else:
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
        self.score = 0
        self.notes = notes
        self.restaurant_id = restaurant_id
        self.user_id = user_id
        self.last_edited = int(time())

    def __repr__(self):
        return '<Dish {}>'.format(self.name)


class UserQuery(BaseQuery, SearchQueryMixin):
    pass


class User(db.Model):
    query_class = UserQuery   
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=True)
    email = db.Column(db.String)
    auth_id = db.Column(db.String)
    date = db.Column(db.Date, nullable=False)
    image = db.Column(db.String, nullable=True)
    about = db.Column(db.String, nullable=True)
    score = db.Column(db.Integer, default=0)
    restaurants = db.relationship('Restaurant', backref='user')
    dishes = db.relationship('Dish', backref='user')
    last_edited = db.Column(db.Integer, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    is_banned = db.Column(db.Boolean, nullable=False)
    search_vector = db.Column(TSVectorType('name', 'email', 'username'))
   
    def __init__(self, name, auth_id, image, email):
        self.name = name
        self.auth_id = auth_id
        self.date = datetime.utcnow()
        self.image = image
        self.email = email
        self.score = 0
        self.last_edited = int(time())
        self.is_admin = False
        self.is_banned = False

    def __repr__(self):
        return '<User {}>'.format(self.name)

    @staticmethod
    def get_or_create(name, auth_id, image, email):
        user = User.query.filter_by(auth_id=auth_id).first()
        if user is None:
            user = User(name, auth_id, image, email)
            db.session.add(user)
            db.session.commit()
        return user
