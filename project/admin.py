from flask import Flask, session, g
from flask_admin import Admin, AdminIndexView, BaseView, expose
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
        return False

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
        return False


class RestaurantView(ModelView):
    
    can_create = False
    column_list = ('id', 'name', 'category', 'image', 'dishes', 'tags', 'user_id', 'last_editor', 'last_edited')

    def __init__(self, session, **kwargs):
        super(RestaurantView, self).__init__(Restaurant, session, **kwargs)


class DishView(ModelView):
    
    can_create = False
    column_list = ('id', 'name', 'price', 'image', 'beef', 'dairy', 'egg',
                   'fish', 'gluten', 'meat', 'nut', 'pork', 'poultry', 'shellfish',
                   'soy', 'wheat', 'score', 'notes', 'restaurant_id', 'user_id', 'last_editor', 'last_edited')

    def __init__(self, session, **kwargs):
        super(DishView, self).__init__(Dish, session, **kwargs)


class UserView(ModelView):
    
    can_create = False
    column_list= ('id', 'name', 'username', 'email', 'image', 'about', 'score',
                  'restaurants', 'dishes', 'is_admin', 'is_banned', 'last_edited')

    def __init__(self, session, **kwargs):
        super(UserView, self).__init__(User, session, **kwargs)
        

admin = Admin(app, name='Admin', index_view=AdminHomeView())
admin.add_view(RestaurantView(db.session, name='Restaurants', category='Database'))
admin.add_view(DishView(db.session, name='Dishes', category='Database'))
admin.add_view(UserView(db.session, name='Users', category='Database'))
