# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
from flask_uploads import configure_uploads, IMAGES, UploadSet

# config
app = Flask(__name__)
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)
GoogleMaps(app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

from project.schema import *
from project.chedible import *
from project.admin import *
import project.google
import project.facebook
