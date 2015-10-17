# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


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
