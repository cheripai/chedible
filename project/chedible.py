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


from flask import render_template, abort, redirect, url_for, request, flash
from flask import session, g
from functools import wraps
from locale import currency
from project import app, db
from project.forms import AddRestaurantForm, AddDishForm, SearchForm
from project.forms import EditUserForm
from project.pagination import Pagination
from project.schema import Restaurant, Dish, User
from time import time


# Global constants
MAX_USERNAME_LENGTH = 12
MAX_QUERIES = 100
PER_PAGE = 5


# This function runs before each request
# If user is logged in, loads user info into global variable g.user
@app.before_request
def load_user():
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


@app.before_request
def load_search_form():
    g.search_form = SearchForm()


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
        # Prevent slashes from breaking routing
        query = ''.join(c for c in g.search_form.query.data if c not in ['/'])
        return redirect(url_for('search_results', table=table, query=query))
    else:
        return redirect(request.referrer)


@app.route('/search_results/<table>/<query>', defaults={'page': 1})
@app.route('/search_results/<table>/<query>/<int:page>')
def search_results(table, query, page):
    message = "No entries found"

    # removes special characters from search to prevent errors
    new_query = ''.join(c for c in query if c.isalnum() or c == ' ')
    if new_query == '':
        return render_template('search.html', message=message, query=query)

    if table == "dishes":
        data = Dish.query.search(new_query, sort=True).limit(MAX_QUERIES)
    elif table == "restaurants":
        data = Restaurant.query.search(new_query, sort=True).limit(MAX_QUERIES)
    elif table == "users":
        data = User.query.search(new_query, sort=True).limit(MAX_QUERIES)
    else:
        abort(404)

    if data.first() is not None:
        message = ""

    pagination = Pagination(page, PER_PAGE, data.count())
    data = split_data(data, page, PER_PAGE, data.count())
    if not data and page != 1:
        abort(404)

    return render_template(
        'search.html',
        message=message,
        data=data,
        query=query,
        table=table,
        pagination=pagination
    )


@app.route('/add', methods=('GET', 'POST'))
@login_required
def add_restaurant():
    form = AddRestaurantForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_restaurant = Restaurant(
                form.name.data,
                form.category.data,
                form.image.data,
                form.tags.data,
                session['user_id']
            )
            new_restaurant.last_editor = session['user_id']
            db.session.add(new_restaurant)
            db.session.commit()
            flash('Thank you for your addition!')
            return redirect(
                url_for('restaurant_profile', id=new_restaurant.id)
            )
    return render_template('restaurant_form.html', form=form)


@app.route('/restaurant/<id>', defaults={'page': 1})
@app.route('/restaurant/<id>/<int:page>')
def restaurant_profile(id, page):
    message = "No entries found"
    restaurant = Restaurant.query.filter_by(id=id).first()
    if restaurant is None:
        abort(404)
    dishes = Dish.query.filter_by(restaurant_id=id).\
        order_by(Dish.score.desc()).order_by(Dish.last_edited.desc())
    if dishes.first() is not None:
        message = ""
    pagination = Pagination(page, PER_PAGE, dishes.count())
    dishes = split_data(dishes, page, PER_PAGE, dishes.count())
    if not dishes and page != 1:
        abort(404)

    return render_template(
        'restaurant_profile.html',
        message=message,
        restaurant=restaurant,
        dishes=dishes,
        pagination=pagination
    )


@app.route('/restaurant/<id>/add', methods=('GET', 'POST'))
@login_required
def add_dish(id):
    form = AddDishForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_dish = Dish(
                form.name.data, form.price.data, form.image.data,
                stb(form.beef.data), stb(form.dairy.data), stb(form.egg.data),
                stb(form.fish.data), stb(form.gluten.data),
                stb(form.meat.data), stb(form.nut.data), stb(form.pork.data),
                stb(form.poultry.data), stb(form.shellfish.data),
                stb(form.soy.data), stb(form.wheat.data), form.notes.data,
                id, session['user_id']
            )
            new_dish.last_editor = session['user_id']
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
            restaurant = Restaurant.query.filter_by(id=id)
            for entry in form:
                if entry.id != "csrf_token":
                    restaurant.update({entry.id: form[entry.id].data})
            restaurant.update({'last_edited': int(time())})
            restaurant.update({'last_editor': session['user_id']})
            r = Restaurant.query.get(id)
            r.editors.append(User.query.get(session['user_id']))
            db.session.commit()
            flash('Thank you for your update!')
            return redirect(url_for('restaurant_profile', id=id))
        return render_template('restaurant_form.html', form=form, id=id)
    if request.method == 'GET':
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant is None:
            abort(404)
        restaurant = rowtodict(restaurant)
        for entry in form:
            if entry.id != "csrf_token":
                form[entry.id].data = restaurant[entry.id]
        return render_template('restaurant_form.html', form=form, id=id)


@app.route('/restaurant/<restaurant_id>/<dish_id>/edit',
           methods=('GET', 'POST'))
@login_required
def edit_dish(restaurant_id, dish_id):
    form = AddDishForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            dish = Dish.query.filter_by(id=dish_id)
            for entry in form:
                if entry.id in ['beef', 'dairy', 'egg', 'fish', 'gluten',
                                'meat', 'nut', 'pork', 'poultry',
                                'shellfish', 'soy', 'wheat']:
                    dish.update({entry.id: stb(form[entry.id].data)})
                elif entry.id == 'price' and form[entry.id].data:
                    dish.update({entry.id: currency(float(form[entry.id].data),
                                grouping=True)})
                elif entry.id != 'csrf_token':
                    dish.update({entry.id: form[entry.id].data})
            dish.update({'last_edited': int(time())})
            dish.update({'last_editor': session['user_id']})
            d = Dish.query.get(dish_id)
            d.editors.append(User.query.get(session['user_id']))
            db.session.commit()
            flash('Thank you for your update!')
            return redirect(url_for('restaurant_profile', id=restaurant_id))
        return render_template(
            'dish_form.html',
            form=form,
            id=restaurant_id,
            dish_id=dish_id
        )
    if request.method == 'GET':
        dish = Dish.query.filter_by(id=dish_id).first()
        if dish is None:
            abort(404)
        dish = rowtodict(dish)
        for entry in form:
            if entry.id == 'price':
                form[entry.id].data = dish[entry.id].replace('$', '').\
                    replace(',', '')
            elif entry.id != "csrf_token":
                form[entry.id].data = dish[entry.id]
        return render_template(
            'dish_form.html',
            form=form,
            id=restaurant_id,
            dish_id=dish_id
        )


@app.route('/user/<id>')
def user_profile(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    month_day_year = User.query.filter_by(id=id).first().\
        date.strftime("%B %d, %Y")

    return render_template(
        'user_profile.html',
        month_day_year=month_day_year,
        user=user
    )


@app.route('/user/<id>/edit', methods=('GET', 'POST'))
@login_required
def edit_user(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    month_day_year = User.query.filter_by(id=id).first().\
        date.strftime("%B %d, %Y")

    form = EditUserForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(id=id)
            for entry in form:
                if entry.id in ['beef', 'dairy', 'egg', 'fish', 'gluten',
                                'meat', 'nut', 'pork', 'poultry',
                                'shellfish', 'soy', 'wheat']:
                    user.update({entry.id: stb(form[entry.id].data)})
                elif entry.id != 'csrf_token':
                    user.update({entry.id: form[entry.id].data})
                user.update({'last_edited': int(time())})
            db.session.commit()
            flash('Thank you for your update!')
            return redirect(url_for('user_profile', id=id))
    else:

        user_dict = rowtodict(user)
        for entry in form:
            if entry.id == "username":
                form.username.data = user.username
            elif entry.id == "about":
                form.about.data = user.about
            elif entry.id != "csrf_token":
                form[entry.id].data = user_dict[entry.id]

    return render_template(
        'edit_user.html',
        form=form,
        month_day_year=month_day_year,
        user=user
    )


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


# Splits data from query for pagination
def split_data(data, cur_page, per_page, total):
    split = [d for d in data]
    begin = (cur_page-1) * per_page
    if begin + per_page < total:
        end = begin + per_page
    else:
        end = total
    return split[begin:end]
