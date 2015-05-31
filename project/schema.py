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
from flask.ext.sqlalchemy import BaseQuery
from locale import currency, LC_ALL, setlocale
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable

make_searchable()

# sets locale for pricing
# may need to modify for internationalization
setlocale(LC_ALL, '')


class RestaurantQuery(BaseQuery, SearchQueryMixin):
    pass


class Restaurant(db.Model):
    query_class = RestaurantQuery
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    dishes = db.relationship('Dish', backref='restaurant')
    tags = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    search_vector = db.Column(TSVectorType('name', 'category', 'tags'))
    # FIXME: should there be location? and how will we reference multiple locations

    def __init__(self, name, category, image, tags, user_id):
        self.name = name
        self.category = category
        self.image = image
        self.tags = tags
        self.user_id = user_id

    def __repr__(self):
        return '<Restaurant {}'.format(self.name)


class DishQuery(BaseQuery, SearchQueryMixin):
    pass


class Dish(db.Model):
    query_class = DishQuery   
    __tablename__ = "dishes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, default=datetime.datetime.utcnow())
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
    notes = db.Column(db.String, nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    search_vector = db.Column(TSVectorType('name'))

    def __init__(self, name, price, image, beef, dairy, egg, fish, gluten, meat, 
                 nut, pork, poultry, shellfish, soy, wheat, notes, restaurant_id, user_id):
        self.name = name
        self.date = datetime.datetime.utcnow()
        self.price = currency(float(price), grouping=True)
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
        self.user_id = user_id

    def __repr__(self):
        return '<Dish {}>'.format(self.name)


class UserQuery(BaseQuery, SearchQueryMixin):
    pass


class User(db.Model):
    query_class = UserQuery   
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    auth_id = db.Column(db.String)
    date = db.Column(db.Date, default=datetime.datetime.utcnow())
    image = db.Column(db.String, nullable=True)
    score = db.Column(db.Integer, default=0)
    restaurants = db.relationship('Restaurant', backref='user')
    dishes = db.relationship('Dish', backref='user')
    search_vector = db.Column(TSVectorType('name', 'email'))
   
    def __init__(self, name, auth_id, image, email):
        self.name = name
        self.auth_id = auth_id
        self.date = datetime.datetime.utcnow()
        self.image = image
        self.email = email
        self.score = 0

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
