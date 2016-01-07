# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import os
from locale import LC_ALL, setlocale


DATABASE = 'data.db'
TEST_DATABASE = 'test.db'
SECRET_KEY = '48e02fc39bae1a191a44277af6b97b1fed08929ee1dc133e733c43e18c496742'
GOOGLE_API_KEY = 'AIzaSyD9-IrWluRI0eKZUAaSGD876n6tGkEiSqY'
FACTUAL_KEY = 'iiwXieyaMjMsIjYGOUFEeMDJZGCaInqO02TRjsKk'
FACTUAL_SECRET = 'B6xI29wWd7lWvHg6gbxEMcrsW16c3Pt5kJQGhSav'
WTF_CSRF_ENABLED = True    # cross-site request forgery prevention

# Constants
MAX_USERNAME_LENGTH = 12
MAX_COMMENT_LENGTH = 512
MAX_QUERIES = 100
PER_PAGE = 10
ADD_RESTAURANT_SCORE = 10
ADD_DISH_SCORE = 10
EDIT_RESTAURANT_SCORE = 5
EDIT_DISH_SCORE = 5
ADD_COMMENT_SCORE = 2
MIN_POST_INTERVAL = 15
DEFAULT_CITY = 'San Francisco, CA, USA'
DEFAULT_COORDS = (37.7749295, -122.4194155)
DEFAULT_RADIUS = 3220
CONTENTS = ['beef', 'dairy', 'egg', 'fish',
            'gluten', 'meat', 'nut', 'non_organic', 'pork',
            'poultry', 'shellfish', 'soy', 'wheat']


# sets locale for pricing
# may need to modify for internationalization
setlocale(LC_ALL, '')

try:
    if int(os.environ['TESTING']) == 1:
        DATABASE_PATH = TEST_DATABASE
    else:
        DATABASE_PATH = DATABASE
except KeyError:
    DATABASE_PATH = DATABASE

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2:///' + DATABASE_PATH
SQLALCHEMY_TRACK_MODIFICATIONS = False
