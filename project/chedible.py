# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import render_template, abort, redirect, url_for, request, flash
from flask import session, g, jsonify
from functools import wraps
from geopy.geocoders import GoogleV3
from locale import currency
from os import path, remove
from profanity import profanity
from project import app, db
from project.forms import AddRestaurantForm, AddDishForm, SearchForm
from project.forms import EditUserForm, AddLocationForm, PhotoForm
from project.factual_places import Places
import project.helpers as h
from project.pagination import Pagination
from project.schema import Restaurant, Dish, User, Comment, Location, Issue
from time import time
from urllib.parse import unquote, quote_plus
from uuid import uuid4
from werkzeug import secure_filename


@app.before_request
def load_user():
    """ This function runs before each request
        If user is logged in, loads user info into global variable g.user
    """
    if 'logged_in' in session and 'user_id' in session:
        g.user = User.query.filter_by(id=session['user_id']).first()
        if g.user.is_banned:
            logout()
        try:
            first, last = g.user.name.split()
        except ValueError:
            first = g.user.name
        if len(g.user.name) > app.config['MAX_USERNAME_LENGTH']:
            g.user.name = first
    else:
        g.user = None


@app.before_request
def load_search_form():
    g.search_form = SearchForm()
    if not g.search_form.location.data:
        try:
            # Sets the location input as the last searched location
            g.search_form.location.data = session['address']
        except KeyError:
            # If no location data available, use default city
            g.search_form.location.data = app.config['DEFAULT_CITY']


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


def login_required(test):
    """ Creates decorator to restrict routes to logged in users
    """

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


@app.route('/test_login/<id>')
def test_login(id):
    """ Used to log in a test user
        Can only be accessed if the TESTING flag is true
    """

    if app.config['TESTING']:
        session['logged_in'] = True
        session['user_id'] = id
    return redirect(url_for('main'))


@app.route('/search/<table>', methods=['POST'])
def search(table):
    """ Route is called when search is initiated on HTML page
        If a query exists, routes user to search results page
    """
    # FIXME: add filtering based on preferences
    # Set geolocator to use Google Geoencoding API
    geolocator = GoogleV3()

    # Prevent slashes from breaking routing
    query = g.search_form.query.data.replace('/', '')

    if g.search_form.validate_on_submit():
        location = geolocator.geocode(g.search_form.location.data)
        radius = g.search_form.radius.data
        search_all = g.search_form.searchAll.data
        if search_all:
            query = 'Restaurants'
        if location:
            session['address'] = location.address
            session['coords'] = (location.latitude, location.longitude)
            return redirect(url_for('search_results',
                                    table=table,
                                    query=query,
                                    coords='{},{}'.format(location.latitude,
                                                          location.longitude),
                                    radius=radius))
        else:
            return render_template(
                'search.html',
                query=query,
                message='Error: Could not find location {}'.format(
                    g.search_form.location.data),
                lat='0',
                lng='0',
                table=table)
    else:
        return redirect(request.referrer)


@app.route('/search_results/<table>/<query>/<coords>/<radius>',
           defaults={'page': 1})
@app.route('/search_results/<table>/<query>/<coords>/<radius>/<int:page>')
def search_results(table, query, coords, radius, page):
    message = "No entries found"
    lat, lng = coords.split(',')
    city_name = h.coords_to_city(lat, lng)
    chedibilitylist, places_coords, places_info = [], [], []
    new_query = quote_plus(query)

    if not new_query:
        return render_template('search.html',
                               message=message,
                               query=query,
                               lat=lat,
                               lng=lng,
                               table=table,
                               radius=radius)

    if table != 'users':
        places = Places(new_query, lat, lng, radius)
        places_names = places.get_names()

    if table == "dishes":
        data = Dish.query.search(query,
                                 sort=True).limit(app.config['MAX_QUERIES'])
        for dish in data:
            chedibilitylist.append(h.is_chedible(dish, g.user))
    elif table == "restaurants":
        data = Restaurant.query.filter(Restaurant.name.ilike('%' + query +
                                                             '%'))
        data = data.union(Restaurant.query.filter(Restaurant.tags.ilike(
            '%' + query + '%')))
        data = data.union(Restaurant.query.filter(Restaurant.category.ilike(
            '%' + query + '%')))
        data = data.union(Restaurant.query.filter(Restaurant.name.in_(
            places_names)))
    elif table == "users":
        data = User.query.search(query,
                                 sort=True).limit(app.config['MAX_QUERIES'])
    else:
        abort(404)

    if data.first() is not None:
        message = ""

    # Remove places not matched in database from map
    data_names = [d.name for d in data]
    places.remove_indices([i for i, name in enumerate(places_names)
                           if name not in data_names])

    places_names = places.get_names()
    places_coords = places.get_coords()
    places_info = places.get_info_boxes()

    pagination = Pagination(page, app.config['PER_PAGE'], data.count())
    data = h.split_data(data, page, app.config['PER_PAGE'], data.count())

    if not data and page != 1:
        abort(404)

    return render_template('search.html',
                           message=message,
                           data=data,
                           chedibilitylist=chedibilitylist,
                           query=query,
                           lat=lat,
                           lng=lng,
                           table=table,
                           radius=radius,
                           pagination=pagination,
                           Restaurant=Restaurant,
                           places_coords=places_coords,
                           places_info=places_info,
                           city_name=city_name)


@app.route('/add', methods=('GET', 'POST'))
@login_required
def add_restaurant():
    form = AddRestaurantForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_restaurant = Restaurant(form.name.data, form.category.data,
                                        form.tags.data, session['user_id'])
            if h.post_interval_exists():
                return render_template('restaurant_form.html', form=form)
            new_restaurant.last_editor = session['user_id']
            db.session.add(new_restaurant)
            h.update_score(app.config['ADD_RESTAURANT_SCORE'])
            db.session.commit()
            flash('Thank you for your addition!')
            return redirect(url_for('restaurant_profile',
                                    id=new_restaurant.id))
    return render_template('restaurant_form.html', form=form)


@app.route('/restaurant/<id>', defaults={'page': 1})
@app.route('/restaurant/<id>/<int:page>')
def restaurant_profile(id, page):
    message = "No entries found"

    restaurant = Restaurant.query.filter_by(id=id).first()
    if restaurant is None:
        abort(404)

    coords = [(loc.lat, loc.lng) for loc in restaurant.locations]

    dishes = Dish.query.filter_by(restaurant_id=id).\
        order_by(Dish.score.desc()).order_by(Dish.last_edited.desc())
    if dishes.first() is not None:
        message = ""

    comments = [
        Comment.query.filter_by(dish_id=d.id).order_by(Comment.id.desc())
        for d in dishes
    ]

    pagination = Pagination(page, app.config['PER_PAGE'], dishes.count())
    dishes = h.split_data(dishes, page, app.config['PER_PAGE'], dishes.count())
    if not dishes and page != 1:
        abort(404)

    # Sets default location to San Francisco
    if 'coords' not in session:
        session['coords'] = app.config['DEFAULT_COORDS']

    lat, lng = session['coords']

    places = Places(restaurant.name, lat, lng, app.config['DEFAULT_RADIUS'])
    places_info = places.get_info_boxes()

    bookmarked = False
    if g.user is not None:
        user = User.query.filter_by(id=g.user.id)
        bookmarks = user.first().bookmarks
        if id in bookmarks:
            bookmarked = True

    return render_template('restaurant_profile.html',
                           message=message,
                           restaurant=restaurant,
                           dishes=dishes,
                           pagination=pagination,
                           comments=comments,
                           User=User,
                           lat=lat,
                           lng=lng,
                           contents=app.config['CONTENTS'],
                           coords=coords,
                           places_info=places_info,
                           bookmarked=bookmarked,
                           MAX_COMMENT_LENGTH=app.config['MAX_COMMENT_LENGTH'])


@app.route('/restaurant/<id>/<coords>/add_location', methods=('GET', 'POST'))
@login_required
def add_location_page(id, coords):
    form = AddLocationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            geolocator = GoogleV3()
            location = geolocator.geocode(form.location.data)
            if location:
                coords = '{},{}'.format(location.latitude, location.longitude)
            else:
                flash('Not a valid location')
    restaurant = Restaurant.query.filter_by(id=id).first()
    lat, lng = coords.split(',')

    places = Places(restaurant.name, lat, lng, app.config['DEFAULT_RADIUS'])
    places_coords = places.get_coords()
    places_info = places.get_add_location_boxes()

    return render_template('restaurant_location.html',
                           form=form,
                           restaurant=restaurant,
                           lat=lat,
                           lng=lng,
                           places_coords=places_coords,
                           places_info=places_info, )


@app.route('/restaurant/<id>/add_location')
@login_required
def add_location(id):
    args = request.args
    try:
        api_id = unquote(args.get('api_id', type=str))
        lat = args.get('lat', type=float)
        lng = args.get('lng', type=float)
        address = args.get('address', type=str)
        if not api_id or lat == None or lng == None or not address:
            return jsonify(status='error')
        new_location = Location(id, api_id, lat, lng, address)
        db.session.add(new_location)
        db.session.commit()
        return jsonify(status='success')
    except (KeyError, TypeError):
        return jsonify(error='Invalid arguments')


@app.route('/restaurant/<restaurant_id>/upload', methods=('GET', 'POST'))
def add_restaurant_photo(restaurant_id):
    form = PhotoForm()
    if request.method == 'POST' and 'photo' in request.files:
        photo = request.files['photo']
        if photo and h.allowed_file_extension(photo.filename):
            filename = str(uuid4()) + path.splitext(secure_filename(
                photo.filename))[-1]
            filepath = path.join(app.config['RESTAURANT_PHOTOS'], filename)
            photo.save(filepath)
            if not h.allowed_file(filepath):
                remove(filepath)
                flash('Invalid file')
            else:
                restaurant = Restaurant.query.filter_by(id=restaurant_id)
                images = list(restaurant.first().images)
                images.append('/'.join(filepath.split('/')[2:]))
                restaurant.update({'images': images})
                db.session.commit()
                flash('File uploaded')
        else:
            flash('Invalid file')
        return redirect(url_for('restaurant_profile',
                                id=restaurant_id,
                                page=1))
    return render_template('upload.html',
                           type='restaurant',
                           form=form,
                           restaurant_id=restaurant_id)


@app.route('/restaurant/<id>/add', methods=('GET', 'POST'))
@login_required
def add_dish(id):
    form = AddDishForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_dish = Dish(form.name.data, form.price.data,
                            h.stb(form.beef.data), h.stb(form.dairy.data),
                            h.stb(form.egg.data), h.stb(form.fish.data),
                            h.stb(form.gluten.data), h.stb(form.meat.data),
                            h.stb(form.nut.data), h.stb(form.non_organic.data),
                            h.stb(form.pork.data), h.stb(form.poultry.data),
                            h.stb(form.shellfish.data), h.stb(form.soy.data),
                            h.stb(form.wheat.data), id, session['user_id'])
            if h.post_interval_exists():
                return render_template('dish_form.html', form=form, id=id)
            new_dish.last_editor = session['user_id']
            db.session.add(new_dish)
            h.update_score(app.config['ADD_DISH_SCORE'])
            db.session.commit()
            flash('Thank you for your addition!')
            return redirect(url_for('restaurant_profile', id=id))
    restaurant = Restaurant.query.filter_by(id=id).first()
    return render_template('dish_form.html',
                           form=form,
                           restaurant=restaurant,
                           id=id)


@app.route('/restaurant/<id>/edit', methods=('GET', 'POST'))
@login_required
def edit_restaurant(id):
    form = AddRestaurantForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if h.post_interval_exists():
                return render_template('restaurant_form.html',
                                       form=form,
                                       id=id)
            restaurant = Restaurant.query.filter_by(id=id)
            for entry in form:
                if entry.id != "csrf_token":
                    restaurant.update({entry.id: form[entry.id].data})
            restaurant.update({'last_edited': int(time())})
            restaurant.update({'last_editor': session['user_id']})
            r = Restaurant.query.get(id)
            r.editors.append(User.query.get(session['user_id']))
            h.update_score(app.config['EDIT_RESTAURANT_SCORE'])
            db.session.commit()
            flash('Thank you for your update!')
            return redirect(url_for('restaurant_profile', id=id))
        return render_template('restaurant_form.html', form=form, id=id)
    if request.method == 'GET':
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant is None:
            abort(404)
        restaurant = h.rowtodict(restaurant)
        for entry in form:
            if entry.id != "csrf_token":
                form[entry.id].data = str(restaurant[entry.id])
        return render_template('restaurant_form.html', form=form, id=id)


@app.route('/restaurant/<restaurant_id>/<dish_id>/edit',
           methods=('GET', 'POST'))
@login_required
def edit_dish(restaurant_id, dish_id):
    form = AddDishForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if h.post_interval_exists():
                return render_template('dish_form.html',
                                       form=form,
                                       id=restaurant_id,
                                       dish_id=dish_id)
            dish = Dish.query.filter_by(id=dish_id)
            for entry in form:
                if entry.id in app.config['CONTENTS']:
                    dish.update({entry.id: h.stb(form[entry.id].data)})
                elif entry.id == 'price' and form[entry.id].data:
                    dish.update({entry.id: currency(
                        float(form[entry.id].data),
                        grouping=True)})
                elif entry.id != 'csrf_token':
                    dish.update({entry.id: form[entry.id].data})
            dish.update({'last_edited': int(time())})
            dish.update({'last_editor': session['user_id']})
            d = Dish.query.get(dish_id)
            d.editors.append(User.query.get(session['user_id']))
            h.update_score(app.config['EDIT_DISH_SCORE'])
            db.session.commit()
            flash('Thank you for your update!')
            return redirect(url_for('restaurant_profile', id=restaurant_id))
        return render_template('dish_form.html',
                               form=form,
                               id=restaurant_id,
                               dish_id=dish_id)
    if request.method == 'GET':
        dish = Dish.query.filter_by(id=dish_id).first()
        restaurant = Restaurant.query.filter_by(id=restaurant_id).first()
        if dish is None:
            abort(404)
        dish = h.rowtodict(dish)
        for entry in form:
            if entry.id == 'price':
                form[entry.id].data = str(dish[entry.id]).replace('$', '').\
                    replace(',', '')
            elif entry.id != "csrf_token":
                form[entry.id].data = str(dish[entry.id])
        return render_template('dish_form.html',
                               form=form,
                               id=restaurant_id,
                               dish_id=dish_id,
                               restaurant=restaurant)


@app.route('/restaurant/<restaurant_id>/<dish_id>/upload',
           methods=('GET', 'POST'))
def add_dish_photo(restaurant_id, dish_id):
    form = PhotoForm()
    if request.method == 'POST' and 'photo' in request.files:
        photo = request.files['photo']
        if photo and h.allowed_file_extension(photo.filename):
            filename = str(uuid4()) + path.splitext(secure_filename(
                photo.filename))[-1]
            filepath = path.join(app.config['DISH_PHOTOS'], filename)
            photo.save(filepath)
            if not h.allowed_file(filepath):
                remove(filepath)
                flash('Invalid file')
            else:
                dish = Dish.query.filter_by(id=dish_id)
                images = list(dish.first().images)
                images.append('/'.join(filepath.split('/')[2:]))
                dish.update({'images': images})
                db.session.commit()
                flash('File uploaded')
        else:
            flash('Invalid file')
        return redirect(url_for('restaurant_profile',
                                id=restaurant_id,
                                page=1))
    return render_template('upload.html',
                           form=form,
                           type='dish',
                           restaurant_id=restaurant_id,
                           dish_id=dish_id)


@app.route('/user/<id>')
def user_profile(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        abort(404)

    user_dict = h.rowtodict(user)

    month_day_year = User.query.filter_by(id=id).first().\
        date.strftime("%B %d, %Y")

    user_opts = [(entry, user_dict[entry]) for entry in app.config['CONTENTS']]

    return render_template('user_profile.html',
                           month_day_year=month_day_year,
                           user=user,
                           user_opts=user_opts)


@app.route('/user/<id>/edit', methods=('GET', 'POST'))
@login_required
def edit_user(id):
    user = User.query.filter_by(id=id).first()

    if user is None or id != str(g.user.id):
        abort(404)
    month_day_year = User.query.filter_by(id=id).first().\
        date.strftime("%B %d, %Y")

    form = EditUserForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            if h.post_interval_exists():
                return render_template('edit_user.html',
                                       form=form,
                                       month_day_year=month_day_year,
                                       user=user)
            user = User.query.filter_by(id=id)
            for entry in form:
                if entry.id in app.config['CONTENTS']:
                    user.update({entry.id: h.stb(form[entry.id].data)})
                elif entry.id != 'csrf_token':
                    user.update({entry.id: form[entry.id].data})
            user.update({'last_edited': int(time())})
            user.update({'last_activity': int(time())})
            user.update({'about': profanity.censor(form['about'].data)})
            db.session.commit()
            flash('Thank you for your update!')
            return redirect(url_for('user_profile', id=id))

    if request.method == 'GET':
        user_dict = h.rowtodict(user)
        for entry in form:
            if entry.id == "username":
                if user.username:
                    form.username.data = user.username
                else:
                    form.username.data = user.name
            elif entry.id == "about":
                form.about.data = user.about
            elif entry.id != "csrf_token":
                form[entry.id].data = str(user_dict[entry.id])

    return render_template('edit_user.html',
                           form=form,
                           month_day_year=month_day_year,
                           user=user)


@app.route('/vote')
@login_required
def vote():
    v = request.args.get('vote', type=str)
    id = request.args.get('id', type=str)
    if id == '':
        return jsonify(error='Invalid id')
    dish = Dish.query.filter_by(id=id)
    try:
        voters = dish.first().voters
        if g.user.id not in voters:
            voters[g.user.id] = None
        # Case 1: User upvotes an unvoted dish
        if v == 'upvote' and voters[g.user.id] is None:
            dish.update({'score': dish.first().score + 1})
            voters[g.user.id] = True
        # Case 2: User removes their upvote
        elif v == 'upvote' and voters[g.user.id] is True:
            dish.update({'score': dish.first().score - 1})
            voters[g.user.id] = None
        # Case 3: User downvotes an unvoted dish
        elif v == 'downvote' and voters[g.user.id] is None:
            dish.update({'score': dish.first().score - 1})
            voters[g.user.id] = False
        # Case 4: User removes their downvote
        elif v == 'downvote' and voters[g.user.id] is False:
            dish.update({'score': dish.first().score + 1})
            voters[g.user.id] = None
        # Case 5: User upvotes downvoted dish
        elif v == 'upvote' and voters[g.user.id] is False:
            dish.update({'score': dish.first().score + 2})
            voters[g.user.id] = True
        # Case 6: User downvotes upvoted dish
        elif v == 'downvote' and voters[g.user.id] is True:
            dish.update({'score': dish.first().score - 2})
            voters[g.user.id] = False
        else:
            return jsonify(error='Invalid type of vote')
        dish.update({'voters': voters})
        db.session.commit()
        return jsonify(result=dish.first().score)
    except (AttributeError, KeyError, TypeError, UnboundLocalError):
        return jsonify(error='Invalid vote or id')


@app.route('/comment')
@login_required
def comment():
    try:
        content = profanity.censor(unquote(request.args.get('content',
                                                            type=str)))
        id = request.args.get('id', type=str)
        if id == '':
            return jsonify(error='Invalid id')
        if len(content) > app.config['MAX_COMMENT_LENGTH']:
            return jsonify(error='Comment exceeds 512 characters')
        if content == '':
            return jsonify(error='Comment must contain text')
        if Dish.query.filter_by(id=id).first() is None:
            return jsonify(error='Dish {} does not exist'.format(id))
        if h.post_interval_exists():
            time_remaining = app.config['MIN_POST_INTERVAL'] - (
                int(time()) - g.user.last_activity)
            return jsonify(
                error='Please wait {} seconds before posting again'.format(
                    time_remaining))
        new_comment = Comment(g.user.id, id, content)
        db.session.add(new_comment)
        h.update_score(app.config['ADD_COMMENT_SCORE'])
        db.session.commit()
        date = new_comment.date.strftime("%B %d, %Y")
        return jsonify(date=date)
    except (KeyError, TypeError):
        return jsonify(error='Invalid content or id')


@app.route('/siftly')
def siftly():
    return render_template('siftly.html')


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/report')
@login_required
def report():
    try:
        type = request.args.get('type', type=str).lower()
        id = request.args.get('id', type=str)
        reason = request.args.get('reason', type=str)
        if type == '':
            return jsonify(error='Type must not contain text')
        if id == '':
            return jsonify(error='Invalid id')
        new_issue = Issue(session['user_id'], type, id, reason)
        db.session.add(new_issue)
        db.session.commit()
        return jsonify(status='success')
    except (KeyError, TypeError):
        return jsonify(error='Invalid type or id')


@app.route('/bookmark')
@login_required
def bookmark():
    try:
        id = request.args.get('id', type=str)
        if id == '':
            return jsonify(error='Invalid id')
        user = User.query.filter_by(id=g.user.id)
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant is None:
            return jsonify(error='Invalid id')
        bookmarks = set(user.first().bookmarks)
        if id in bookmarks:
            bookmarks.remove(id)
        else:
            bookmarks.add(id)
        user.update({'bookmarks': set(bookmarks)})
        db.session.commit()
        return jsonify(status='success')
    except KeyError:
        return jsonify(error='Invalid id')


@app.route('/bookmarks/<id>')
@login_required
def bookmarks(id):
    if str(g.user.id) != id:
        abort(404)
    message = "No entries found"
    user = User.query.filter_by(id=g.user.id)
    bookmarks = user.first().bookmarks
    if len(bookmarks) != 0:
        message = ""
    data = Restaurant.query.filter(Restaurant.id.in_(bookmarks)).all()
    return render_template('bookmarks.html', data=data, message=message)
