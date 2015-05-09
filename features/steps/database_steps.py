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


from behave import *
from project.schema import Restaurant, Dish, User


@when(u'we add "{text}" to "{table}"')
def db_add(context, text, table):
    if table == "restaurants":
        entry = Restaurant(text, 'test', 'test')
    elif table == "dishes":
        entry = Dish(text, 0.00, '', None, None, None, None, None, 
                     None, None, None, None, None, None, None, '', 0, 0)  
    else:
        entry = User(text, '')
    context.db.session.add(entry)


@when(u'we delete "{text}" from "{table}"')
def db_delete(context, text, table):
    if table == "restaurants":
        entry = context.db.session.query(Restaurant).filter_by(name=text)
    elif table == "dishes":
        entry = context.db.session.query(Dish).filter_by(name=text)
    else:
        entry = context.db.session.query(User).filter_by(name=text)
    entry.delete()


@then(u'we should see "{text}" in "{table}"')
def db_add_check(context, text, table):
    if table == "restaurants":
        assert text in str(context.db.session.query(Restaurant).first().name)
    elif table == "dishes":
        assert text in str(context.db.session.query(Dish).first().name)
    else:
        assert text in str(context.db.session.query(User).first().name)


@then(u'we should not see "{text}" in "{table}"')
def db_delete_check(context, text, table):
    if table == "restaurants":
        assert context.db.session.query(Restaurant).filter_by(name=text).first() is None
    elif table == "dishes":
        assert context.db.session.query(Dish).filter_by(name=text).first() is None
    else:
        assert context.db.session.query(User).filter_by(name=text).first() is None