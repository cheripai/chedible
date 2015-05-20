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
from project.schema import Restaurant, Dish, User


def db_create():
    db.drop_all()
    db.configure_mappers()
    db.create_all()

    '''   
    for i in range(50):
        if i % 2 == 0:
            entry = Restaurant('test {}'.format(i), 'vegetarian', 'img')
        else:
            entry = Restaurant('test {}'.format(i), 'vegan', 'img')
        db.session.add(entry)
    '''

    db.session.commit()


if __name__ == "__main__":
    db_create()
