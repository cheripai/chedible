# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from project import db
from project.schema import *


def db_create():
    db.drop_all()
    db.configure_mappers()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    db_create()
