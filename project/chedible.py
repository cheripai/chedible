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


from flask import Flask, render_template, redirect, url_for, request, flash, session, g
from functools import wraps
from locale import currency
from project import app, db
from project.forms import AddRestaurantForm, AddDishForm, SearchForm
from project.google import *
from project.facebook import *
from project.schema import Restaurant, Dish, User
from sqlalchemy_searchable import search


# Global constants
MAX_USERNAME_LENGTH = 12
MAX_QUERIES = 50


# This function runs before each request
# If user is logged in, loads user info into global variable g.user
@app.before_request
def load_user():
    g.search_form = SearchForm()
    if 'logged_in' in session and 'user_id' in session:
        g.user = User.query.filter_by(id=session['user_id']).first()
        
        first, last = g.user.name.split()

        if len(g.user.name) > MAX_USERNAME_LENGTH:
            g.user.name = first
        
        if len(g.user.name) > MAX_USERNAME_LENGTH:
            charlist = []
            charlist[:0] = first

            while len(charlist) > MAX_USERNAME_LENGTH - 3:
                del charlist[-1]

            g.user.name = ''.join(charlist) + '...'
    else:
        g.user = None


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Creates decorator to restrict routes to logged in users
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to be logged in to do that!')
            return redirect(url_for('main'))
    return wrap


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    flash('Logged out')
    session.pop('logged_in', None)
    return redirect(url_for('main'))


# Used to log in a test user
# Can only be accessed if the TESTING flag is true
@app.route('/test_login/<id>')
def test_login(id):
    if app.config['TESTING']:
        session['logged_in'] = True
        session['user_id'] = id
    return redirect(url_for('main'))


# Route is called when search is initiated on HTML page
# If a query exists, routes user to search results page
@app.route('/search/<table>', methods=['POST'])
def search(table):
    # We need to add filtering based on preferences
    if g.search_form.validate_on_submit():
        return redirect(url_for('search_results', table=table, query=g.search_form.query.data))
    else:
        return redirect(url_for('main'))


@app.route('/search_results/<table>/<query>')
def search_results(table, query):
    message = "No entries found"

    # removes special characters from search to prevent errors
    stripped_query = ''.join(c for c in query if c.isalnum() or c == ' ')
    if stripped_query == '':
        return render_template('search.html', message=message, query=query)
        
    if table == "dishes":
        data = Dish.query.search(stripped_query, sort=True).limit(MAX_QUERIES)
    elif table == "restaurants":
        data = Restaurant.query.search(stripped_query, sort=True).limit(MAX_QUERIES)
    elif table == "users":
        data = User.query.search(stripped_query, sort=True).limit(MAX_QUERIES)
    elif table =="all":
        # FIXME: Add search all tables
        data = Dish.query.search('FIXME', sort=True).limit(MAX_QUERIES)
        message = "I'm not implemented yet!"
    else:
        return render_template('search.html', message=message)

    if data.first() is not None:
        message = ""

    return render_template('search.html', message=message, data=data, query=query)


@app.route('/add', methods=('GET', 'POST'))
@login_required
def add_restaurant():
    form = AddRestaurantForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_restaurant = Restaurant(form.name.data, form.category.data, form.image.data, form.tags.data, session['user_id'])
            db.session.add(new_restaurant)
            db.session.commit()
            flash('Thank you for your addition!')
            return redirect(url_for('restaurant_profile', id=new_restaurant.id))
    return render_template('restaurant_form.html', form=form)


@app.route('/restaurant/<id>')
def restaurant_profile(id):
    message = "No entries found"
    restaurant = Restaurant.query.filter_by(id=id).first()
    dishes = Dish.query.filter_by(restaurant_id=id)

    if dishes.first() is not None:
        message = ""

    return render_template('restaurant_profile.html', message=message, restaurant=restaurant, dishes=dishes)


@app.route('/restaurant/<id>/add', methods=('GET', 'POST'))
@login_required
def add_dish(id):
    form = AddDishForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_dish = Dish(form.name.data, form.price.data, form.image.data, stb(form.beef.data),
                            stb(form.dairy.data), stb(form.egg.data), stb(form.fish.data),
                            stb(form.gluten.data), stb(form.meat.data), stb(form.nut.data),
                            stb(form.pork.data), stb(form.poultry.data), stb(form.shellfish.data),
                            stb(form.soy.data), stb(form.wheat.data), form.notes.data, 
                            id, session['user_id'])
            db.session.add(new_dish)
            db.session.commit()
            flash('Thank you for your addition!')
            return redirect(url_for('restaurant_profile', id=id))
    return render_template('dish_form.html', form=form, id=id)


@app.route('/restaurant/<id>/edit', methods=('GET', 'POST'))
@login_required
def edit_restaurant(id):
    form = AddRestaurantForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            for entry in form:
                if entry.id != "csrf_token":
                    Restaurant.query.filter_by(id=id).update({entry.id: form[entry.id].data})
            Restaurant.query.filter_by(id=id).update({'user_id': session['user_id']})
            db.session.commit()
            flash('Thank you for your update!')
            return redirect(url_for('restaurant_profile', id=id))
    restaurant = rowtodict(Restaurant.query.filter_by(id=id).first())
    for entry in form:
        if entry.id != "csrf_token":
            form[entry.id].data = restaurant[entry.id]
    return render_template('restaurant_form.html', form=form, id=id)


@app.route('/restaurant/<restaurant_id>/<dish_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_dish(restaurant_id, dish_id):
    form = AddDishForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            for entry in form:
                if entry.id in ['beef', 'dairy', 'egg', 'fish', 'gluten', 'meat',
                                'nut', 'pork', 'poultry', 'shellfish', 'soy', 'wheat']:
                    Dish.query.filter_by(id=dish_id).update({entry.id: stb(form[entry.id].data)})
                elif entry.id == 'price' and form[entry.id].data:
                    Dish.query.filter_by(id=dish_id).update({entry.id: currency(float(form[entry.id].data), grouping=True)})
                elif entry.id != 'csrf_token':
                    Dish.query.filter_by(id=dish_id).update({entry.id: form[entry.id].data})
            Dish.query.filter_by(id=dish_id).update({'user_id': session['user_id']})
            db.session.commit()
            flash('Thank you for your update!')
            return redirect(url_for('restaurant_profile', id=restaurant_id))
    dish = rowtodict(Dish.query.filter_by(id=dish_id).first())
    for entry in form:
        if entry.id == 'price':
            form[entry.id].data = dish[entry.id].replace('$', '').replace(',', '')
        elif entry.id != "csrf_token":
            form[entry.id].data = dish[entry.id]
    return render_template('dish_form.html', form=form, id=restaurant_id, dish_id=dish_id)


@app.route('/user/<id>')
def user_profile(id):
    #g.user holds user data
    month_day_year = User.query.filter_by(id=id).first().date.strftime("%B %d, %Y")

    return render_template('user_profile.html', month_day_year=month_day_year)


# Convert string value from HTML form to boolean value
def stb(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    elif s == 'None':
        return None
    else:
        return ValueError


# Converts a sqlalchemy row into a dictionary for iteration
def rowtodict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d
