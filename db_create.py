# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from project import db
from project.schema import *


def db_create():
    db.drop_all()
    db.configure_mappers()
    db.create_all()

    '''
    for i in range(50):
        if i % 4 == 0:
            entry = Restaurant('test {}'.format(i), 'vegetarian', '', '', None)
        elif i % 4 == 1:
            entry = Restaurant('test {}'.format(i), 'vegan', None, '', None)
        elif i % 4 == 2:
            entry = User('test {}'.format(i), '0{}'.format(i), None,
                         'email{}@email.org'.format(i))
        else:
            entry = Dish('testdish{}'.format(i), '0.00', '', None, True, None,
                         False, False, True, False, True, None, None, None,
                         None, 1, 1)
        db.session.add(entry)
    '''

    db.session.commit()


if __name__ == "__main__":
    db_create()
