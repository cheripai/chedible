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
