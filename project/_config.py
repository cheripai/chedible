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


import os
from locale import LC_ALL, setlocale


DATABASE = 'data.db'
TEST_DATABASE = 'test.db'
SECRET_KEY = '48e02fc39bae1a191a44277af6b97b1fed08929ee1dc133e733c43e18c496742'
WTF_CSRF_ENABLED = True    # cross-site request forgery prevention

# Constants
MAX_USERNAME_LENGTH = 12
MAX_COMMENT_LENGTH = 512
MAX_QUERIES = 100
PER_PAGE = 5
ADD_RESTAURANT_SCORE = 10
ADD_DISH_SCORE = 10
EDIT_RESTAURANT_SCORE = 5
EDIT_DISH_SCORE = 5
ADD_COMMENT_SCORE = 2
MIN_POST_INTERVAL = 15
DEFAULT_CITY = 'San Francisco'
CONTENTS = ['beef', 'dairy', 'egg', 'fish',
            'gluten', 'meat', 'nut', 'pork',
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
