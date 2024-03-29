# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from datetime import datetime
from flask_sqlalchemy import BaseQuery
from locale import currency
import os
from project import app, db
from sqlalchemy_searchable import SearchQueryMixin, make_searchable
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils.types import TSVectorType
from time import time
import uuid

make_searchable()

try:
    if int(os.environ['TESTING']) == 1:
        restaurants_users = db.Table(
            'restaurants_users', db.Column('restaurants_id', db.Integer,
                                           db.ForeignKey('restaurants.id')),
            db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
            db.PrimaryKeyConstraint('restaurants_id', 'users_id'))

        dishes_users = db.Table(
            'dishes_users',
            db.Column('dishes_id', db.Integer, db.ForeignKey('dishes.id')),
            db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
            db.PrimaryKeyConstraint('dishes_id', 'users_id'))
except KeyError:
    restaurants_users = db.Table(
        'restaurants_users',
        db.Column('restaurants_id', UUIDType, db.ForeignKey('restaurants.id')),
        db.Column('users_id', UUIDType, db.ForeignKey('users.id')),
        db.PrimaryKeyConstraint('restaurants_id', 'users_id'))

    dishes_users = db.Table(
        'dishes_users',
        db.Column('dishes_id', UUIDType, db.ForeignKey('dishes.id')),
        db.Column('users_id', UUIDType, db.ForeignKey('users.id')),
        db.PrimaryKeyConstraint('dishes_id', 'users_id'))


class RestaurantQuery(BaseQuery, SearchQueryMixin):
    pass


class Restaurant(db.Model):
    query_class = RestaurantQuery
    __tablename__ = "restaurants"

    try:
        if int(os.environ['TESTING']) == 1:
            id = db.Column(db.Integer, primary_key=True)
    except KeyError:
        id = db.Column(UUIDType(binary=False), primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String, nullable=True)
    images = db.Column(db.PickleType, nullable=True)
    dishes = db.relationship('Dish',
                             cascade="all, delete, delete-orphan",
                             backref='restaurant')
    tags = db.Column(db.String, nullable=True)
    editors = db.relationship('User',
                              backref='restaurant',
                              secondary=restaurants_users)
    locations = db.relationship('Location', backref='restaurant')
    last_edited = db.Column(db.Integer, nullable=False)
    try:
        if int(os.environ['TESTING']) == 1:
            last_editor = db.Column(db.Integer)
    except KeyError:
        last_editor = db.Column(UUIDType)
    search_vector = db.Column(TSVectorType('name',
                                           'category',
                                           'tags',
                                           weights={'name': 'A',
                                                    'category': 'C',
                                                    'tags': 'B'}))

    def __init__(self, name, category, tags, user_id):
        if app.config['TESTING'] != True:
            self.id = uuid.uuid4()
        self.name = name
        self.date = datetime.utcnow()
        self.category = category
        self.images = []
        self.tags = tags
        if user_id is None:
            self.editors = []
        else:
            self.editors.append(User.query.get(user_id))
        self.last_edited = int(time())

    def __repr__(self):
        return '<Restaurant {}>'.format(self.id)


class DishQuery(BaseQuery, SearchQueryMixin):
    pass


class Dish(db.Model):
    query_class = DishQuery
    __tablename__ = "dishes"

    try:
        if int(os.environ['TESTING']) == 1:
            id = db.Column(db.Integer, primary_key=True)
            restaurant_id = db.Column(db.Integer,
                                      db.ForeignKey('restaurants.id'))
    except KeyError:
        id = db.Column(UUIDType(binary=False), primary_key=True)
        restaurant_id = db.Column(UUIDType, db.ForeignKey('restaurants.id'))
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    price = db.Column(db.String, nullable=True)
    images = db.Column(db.PickleType, nullable=True)
    beef = db.Column(db.Boolean, nullable=True)
    dairy = db.Column(db.Boolean, nullable=True)
    egg = db.Column(db.Boolean, nullable=True)
    fish = db.Column(db.Boolean, nullable=True)
    gluten = db.Column(db.Boolean, nullable=True)
    meat = db.Column(db.Boolean, nullable=True)
    nut = db.Column(db.Boolean, nullable=True)
    non_organic = db.Column(db.Boolean, nullable=True)
    pork = db.Column(db.Boolean, nullable=True)
    poultry = db.Column(db.Boolean, nullable=True)
    shellfish = db.Column(db.Boolean, nullable=True)
    soy = db.Column(db.Boolean, nullable=True)
    wheat = db.Column(db.Boolean, nullable=True)
    score = db.Column(db.Integer)
    editors = db.relationship('User', backref='dish', secondary=dishes_users)
    last_edited = db.Column(db.Integer, nullable=False)
    voters = db.Column(db.PickleType, nullable=True)
    try:
        if int(os.environ['TESTING']) == 1:
            last_editor = db.Column(db.Integer)
    except KeyError:
        last_editor = db.Column(UUIDType)
    commenters = db.relationship('Comment', backref='dish')
    search_vector = db.Column(TSVectorType('name'))

    def __init__(self, name, price, beef, dairy, egg, fish, gluten, meat, nut,
                 non_organic, pork, poultry, shellfish, soy, wheat,
                 restaurant_id, user_id):
        if app.config['TESTING'] != True:
            self.id = uuid.uuid4()
        self.name = name
        self.date = datetime.utcnow()
        if price:
            self.price = currency(float(price), grouping=True)
        else:
            self.price = price
        self.images = []
        self.beef = beef
        self.dairy = dairy
        self.egg = egg
        self.fish = fish
        self.gluten = gluten
        self.meat = meat
        self.nut = nut
        self.non_organic = non_organic
        self.pork = pork
        self.poultry = poultry
        self.shellfish = shellfish
        self.soy = soy
        self.wheat = wheat
        self.score = 0
        self.restaurant_id = restaurant_id
        if user_id is None:
            self.editors = []
        else:
            self.editors.append(User.query.get(user_id))
        self.last_edited = int(time())
        self.voters = {}

    def __repr__(self):
        return '<Dish {}>'.format(self.id)


class UserQuery(BaseQuery, SearchQueryMixin):
    pass


class User(db.Model):
    query_class = UserQuery
    __tablename__ = "users"

    try:
        if int(os.environ['TESTING']) == 1:
            id = db.Column(db.Integer, primary_key=True)
    except KeyError:
        id = db.Column(UUIDType(binary=False), primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=True)
    email = db.Column(db.String)
    auth_id = db.Column(db.String)
    date = db.Column(db.Date, nullable=False)
    image = db.Column(db.String, nullable=True)
    beef = db.Column(db.Boolean, nullable=True)
    dairy = db.Column(db.Boolean, nullable=True)
    egg = db.Column(db.Boolean, nullable=True)
    fish = db.Column(db.Boolean, nullable=True)
    gluten = db.Column(db.Boolean, nullable=True)
    meat = db.Column(db.Boolean, nullable=True)
    nut = db.Column(db.Boolean, nullable=True)
    non_organic = db.Column(db.Boolean, nullable=True)
    pork = db.Column(db.Boolean, nullable=True)
    poultry = db.Column(db.Boolean, nullable=True)
    shellfish = db.Column(db.Boolean, nullable=True)
    soy = db.Column(db.Boolean, nullable=True)
    wheat = db.Column(db.Boolean, nullable=True)
    about = db.Column(db.String, nullable=True)
    score = db.Column(db.Integer, default=0)
    restaurants = db.relationship('Restaurant',
                                  backref='user',
                                  viewonly=True,
                                  secondary=restaurants_users)
    dishes = db.relationship('Dish',
                             backref='user',
                             viewonly=True,
                             secondary=dishes_users)
    bookmarks = db.Column(db.PickleType, nullable=True)
    last_edited = db.Column(db.Integer, nullable=False)
    last_activity = db.Column(db.Integer, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    is_banned = db.Column(db.Boolean, nullable=False)
    search_vector = db.Column(TSVectorType('name',
                                           'email',
                                           'username',
                                           weights={'name': 'B',
                                                    'email': 'A',
                                                    'username': 'A'}))

    def __init__(self, name, auth_id, image, email):
        if app.config['TESTING'] != True:
            self.id = uuid.uuid4()
        self.name = name
        self.auth_id = auth_id
        self.date = datetime.utcnow()
        self.image = image
        self.beef = None
        self.dairy = None
        self.egg = None
        self.fish = None
        self.gluten = None
        self.meat = None
        self.nut = None
        self.non_organic = None
        self.pork = None
        self.poultry = None
        self.shellfish = None
        self.soy = None
        self.wheat = None
        self.email = email
        self.score = 0
        self.last_edited = int(time())
        self.last_activity = int(time() - 100)
        self.is_admin = False
        self.is_banned = False
        self.about = "I love chedible!"
        self.voters = {}
        self.bookmarks = {}

    def __repr__(self):
        return '<User {}>'.format(self.id)

    @staticmethod
    def get_or_create(name, auth_id, image, email):
        user = User.query.filter_by(auth_id=auth_id).first()
        if user is None:
            user = User(name, auth_id, image, email)
            db.session.add(user)
            db.session.commit()
        return user


class Comment(db.Model):

    __tablename__ = "comments"

    try:
        if int(os.environ['TESTING']) == 1:
            id = db.Column(db.Integer, primary_key=True)
            user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
            dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'))
    except KeyError:
        id = db.Column(UUIDType(binary=False), primary_key=True)
        user_id = db.Column(UUIDType, db.ForeignKey('users.id'))
        dish_id = db.Column(UUIDType, db.ForeignKey('dishes.id'))
    date = db.Column(db.Date, nullable=False)
    content = db.Column(db.String, nullable=False)

    def __init__(self, user_id, dish_id, content):
        if app.config['TESTING'] == False:
            self.id = uuid.uuid4()
        self.date = datetime.utcnow()
        self.user_id = user_id
        self.dish_id = dish_id
        self.content = content

    def __repr__(self):
        return '<Comment {}>'.format(self.id)


class Location(db.Model):

    __tablename__ = "locations"

    try:
        if int(os.environ['TESTING']) == 1:
            id = db.Column(db.Integer, primary_key=True)
            restaurant_id = db.Column(db.Integer,
                                      db.ForeignKey('restaurants.id'))
    except KeyError:
        id = db.Column(UUIDType(binary=False), primary_key=True)
        restaurant_id = db.Column(UUIDType, db.ForeignKey('restaurants.id'))
    date = db.Column(db.Date, nullable=False)
    api_id = db.Column(db.String, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    address = db.Column(db.String, nullable=False)

    def __init__(self, restaurant_id, api_id, lat, lng, address):
        if app.config['TESTING'] == False:
            self.id = uuid.uuid4()
        self.date = datetime.utcnow()
        self.restaurant_id = restaurant_id
        self.api_id = api_id
        self.lat = lat
        self.lng = lng
        self.address = address

    def __repr__(self):
        return '<Location {}>'.format(self.id)


class Issue(db.Model):

    __tablename__ = "issues"

    try:
        if int(os.environ['TESTING']) == 1:
            id = db.Column(db.Integer, primary_key=True)
            user_id = db.Column(db.Integer, nullable=False)
            type_id = db.Column(db.Integer, nullable=False)
    except KeyError:
        id = db.Column(UUIDType(binary=False), primary_key=True)
        user_id = db.Column(UUIDType, nullable=False)
        type_id = db.Column(UUIDType, nullable=False)
    date = db.Column(db.Date, nullable=False)
    type = db.Column(db.String, nullable=False)
    content = db.Column(db.String)

    def __init__(self, user_id, type, type_id, content):
        if app.config['TESTING'] == False:
            self.id = uuid.uuid4()
        self.date = datetime.utcnow()
        self.user_id = user_id
        self.type = type
        self.type_id = type_id
        self.content = content

    def __repr__(self):
        return '<Issue {}>'.format(self.id)
