# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import session, g, flash
import json
from imghdr import what
from project import app, db
from project.schema import Restaurant, Dish, User, Comment, Location, Issue
from time import time
from urllib.request import urlopen


def stb(s):
    """ Convert string value from HTML form to boolean value
    """
    if s == 'True':
        return True
    elif s == 'False':
        return False
    elif s == 'None':
        return None
    else:
        return ValueError


def rowtodict(row):
    """ Converts a sqlalchemy row into a dictionary for iteration
    """
    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)
    return d


def split_data(data, cur_page, per_page, total):
    """ Splits data from query for pagination
    """
    split = [d for d in data]
    begin = (cur_page - 1) * per_page
    if begin + per_page < total:
        end = begin + per_page
    else:
        end = total
    return split[begin:end]


def is_chedible(dish, user):
    """ If the dish contains an item, and the user does not want the item
            Not chedible
        If the dish might contain the item, and the user does not want the item
            Not chedible
        Else
            Chedible
    """
    if user is None or dish is None:
        return None
    dish = rowtodict(dish)
    user = rowtodict(user)
    for entry in app.config['CONTENTS']:
        if (dish[entry] and not user[entry]) or \
           (dish[entry] is None and not user[entry]):
            return False
    return True


def update_score(amt):
    user = User.query.filter_by(id=session['user_id']).first()
    user.score += amt
    # Updating the user's score also updates their last activity
    user.last_activity = int(time())


def post_interval_exists():
    # Allows test cases to post without waiting for interval
    if app.config['TESTING']:
        return False
    if int(time()) - g.user.last_activity < app.config['MIN_POST_INTERVAL']:
        time_remaining = app.config['MIN_POST_INTERVAL'] - (
            int(time()) - g.user.last_activity)
        message = 'Please wait {} seconds before posting again'.format(
            time_remaining)
        flash(message)
        return True
    return False


def coords_to_city(lat, lng):
    openstreetmap = 'https://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}'
    response = urlopen(openstreetmap.format(lat, lng))
    data = json.loads(response.read().decode('utf-8'))
    try:
        return data['address']['city']
    except KeyError:
        return ''


def allowed_file_extension(filename):
    """ Checks whether file extension is in list of allowed extensions
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def allowed_file(filepath):
    """ Checks file header to see if it is an image file
    """
    image_type = what(filepath)
    if not image_type:
        return False
    else:
        return True
