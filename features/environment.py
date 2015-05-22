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
import sys
import tempfile

pwd = os.path.abspath(os.path.dirname(__file__))
project = os.path.basename(pwd)
full_path = pwd.strip(project)

# We set the env variable testing to true 
# so that project/_config.py will connect to the test database
os.environ['TESTING'] = '1'


try:
    from project import app, db
    from db_create import db_create
except ImportError:
    sys.path.append(full_path)
    from project import app, db
    from db_create import db_create


def before_feature(context, feature):
    app.config['DEBUG'] = False
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    context.client = app.test_client()
    context.db = db
    db_create()
    

def after_feature(context, feature):
    os.environ['TESTING'] = '0'
    context.db.session.close()
    context.db.drop_all()
