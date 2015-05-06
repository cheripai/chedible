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

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'data.db'
TEST_DATABASE = 'test.db'

try:
    os.environ['TESTING']
    if int(os.environ['TESTING']) == 1:
        DATABASE_PATH = os.path.join(basedir, TEST_DATABASE)
    else:
        DATABASE_PATH = os.path.join(basedir, DATABASE)
except KeyError:
    DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
