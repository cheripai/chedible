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
from project import app
from locale import currency, LC_ALL, setlocale


DATABASE = 'data.db'
TEST_DATABASE = 'test.db'
SECRET_KEY = '\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16'
WTF_CSRF_ENABLED = True    # cross-site request forgery prevention

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

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://localhost/' + DATABASE_PATH
