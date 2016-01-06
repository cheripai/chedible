# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from flask import session, g, abort
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from project import app, db
from project.schema import *


class AdminHomeView(AdminIndexView):

    def is_accessible(self):
        if app.config['DEBUG']:
            return True
        if session['logged_in']:
            if g.user.is_admin:
                return True
        abort(404)

    @expose('/')
    def index(self):
        return self.render('admin.html')


class ModelView(ModelView):

    def is_accessible(self):
        if app.config['DEBUG']:
            return True
        if session['logged_in']:
            if g.user.is_admin:
                return True
        abort(404)


class RestaurantView(ModelView):

    can_create = False
    column_list = ('id', 'name', 'category', 'image', 'dishes', 'tags', 'locations', 'editors', 'last_editor', 'last_edited')

    def __init__(self, session, **kwargs):
        super(RestaurantView, self).__init__(Restaurant, session, **kwargs)


class DishView(ModelView):

    can_create = False
    column_list = ('id', 'name', 'price', 'image', 'beef', 'dairy', 'egg',
                   'fish', 'gluten', 'meat', 'nut', 'organic', 'pork', 'poultry', 'shellfish',
                   'soy', 'wheat', 'score', 'restaurant_id', 'editors', 'last_editor', 'last_edited')

    def __init__(self, session, **kwargs):
        super(DishView, self).__init__(Dish, session, **kwargs)


class UserView(ModelView):

    can_create = False
    column_list = ('id', 'name', 'username', 'email', 'image', 'about', 'score',
                  'restaurants', 'dishes', 'is_admin', 'is_banned', 'last_edited')

    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)


class CommentView(ModelView):

    can_create = False
    column_list = ('id', 'date', 'user_id', 'dish_id', 'content')

    def __init__(self, session, **kwargs):
        super(CommentView, self).__init__(Comment, session, **kwargs)


class LocationView(ModelView):

    can_create = False
    column_list = ('id', 'date', 'restaurant_id', 'api_id', 'lat', 'lng', 'address')

    def __init__(self, session, **kwargs):
        super(LocationView, self).__init__(Location, session, **kwargs)


admin = Admin(app, name='Admin', index_view=AdminHomeView())
admin.add_view(RestaurantView(db.session, name='Restaurants', category='Database'))
admin.add_view(DishView(db.session, name='Dishes', category='Database'))
admin.add_view(UserView(db.session, name='Users', category='Database'))
admin.add_view(CommentView(db.session, name='Comments', category='Database'))
admin.add_view(LocationView(db.session, name='Locations', category='Database'))
