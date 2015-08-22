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
from flask.ext.sqlalchemy import BaseQuery
from locale import currency
from project import db
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable
from time import time


make_searchable()


restaurants_users = db.Table(
    'restaurants_users',
    db.Column('restaurants_id', db.Integer, db.ForeignKey('restaurants.id')),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
    db.PrimaryKeyConstraint('restaurants_id', 'users_id')
)


dishes_users = db.Table(
    'dishes_users',
    db.Column('dishes_id', db.Integer, db.ForeignKey('dishes.id')),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id')),
    db.PrimaryKeyConstraint('dishes_id', 'users_id')
)


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
    dishes = db.relationship(
        'Dish',
        cascade="all, delete, delete-orphan",
        backref='restaurant'
    )
    tags = db.Column(db.String, nullable=True)
    editors = db.relationship(
        'User',
        backref='restaurant',
        secondary=restaurants_users
    )
    last_edited = db.Column(db.Integer, nullable=False)
    last_editor = db.Column(db.Integer)
    search_vector = db.Column(
        TSVectorType('name', 'category', 'tags',
                     weights={'name': 'A', 'category': 'C', 'tags': 'B'})
    )
    # FIXME: should there be location? and how to reference multiple locations

    def __init__(self, name, category, image, tags, user_id):
        self.name = name
        self.date = datetime.utcnow()
        self.category = category
        self.image = image
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
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    editors = db.relationship(
        'User',
        backref='dish',
        secondary=dishes_users
    )
    last_edited = db.Column(db.Integer, nullable=False)
    voters = db.Column(db.PickleType, nullable=True)
    last_editor = db.Column(db.Integer)
    commenters = db.relationship('Comment', backref='dish')
    search_vector = db.Column(TSVectorType('name'))

    def __init__(self, name, price, image, beef, dairy, egg,
                 fish, gluten, meat, nut, pork, poultry, shellfish,
                 soy, wheat, restaurant_id, user_id):
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

    id = db.Column(db.Integer, primary_key=True)
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
    pork = db.Column(db.Boolean, nullable=True)
    poultry = db.Column(db.Boolean, nullable=True)
    shellfish = db.Column(db.Boolean, nullable=True)
    soy = db.Column(db.Boolean, nullable=True)
    wheat = db.Column(db.Boolean, nullable=True)
    about = db.Column(db.String, nullable=True)
    score = db.Column(db.Integer, default=0)
    restaurants = db.relationship(
        'Restaurant',
        backref='user',
        viewonly=True,
        secondary=restaurants_users
    )
    dishes = db.relationship(
        'Dish',
        backref='user',
        viewonly=True,
        secondary=dishes_users
    )
    last_edited = db.Column(db.Integer, nullable=False)
    last_activity = db.Column(db.Integer, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    is_banned = db.Column(db.Boolean, nullable=False)
    search_vector = db.Column(
        TSVectorType('name', 'email', 'username',
                     weights={'name': 'B', 'email': 'A', 'username': 'A'})
    )

    def __init__(self, name, auth_id, image, email):
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
        self.pork = None
        self.poultry = None
        self.shellfish = None
        self.soy = None
        self.wheat = None
        self.email = email
        self.score = 0
        self.last_edited = int(time())
        self.last_activity = int(time())
        self.is_admin = False
        self.is_banned = False
        self.about = "I love chedible!"

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

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dish_id = db.Column(db.Integer, db.ForeignKey('dishes.id'))
    content = db.Column(db.String, nullable=False)

    def __init__(self, user_id, dish_id, content):
        self.date = datetime.utcnow()
        self.user_id = user_id
        self.dish_id = dish_id
        self.content = content

    def __repr__(self):
        return '<Comment {}>'.format(self.id)
