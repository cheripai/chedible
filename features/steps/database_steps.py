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
from project.chedible import rowtodict
from project.schema import Restaurant, Dish, User


@when(u'we add "{text}" to "{table}"')
def db_add(context, text, table):
    if table == "restaurants":
        entry = Restaurant(text, 'test', 'test', 'test', None)
    elif table == "dishes":
        entry = Dish(text, 0.00, '', None, None, None, None, None,
                     None, None, None, None, None, None, None, '', None, None)
    else:
        entry = User(text, '', '', '')
    context.db.session.add(entry)
    context.db.session.commit()


@when(u'we delete "{text}" from "{table}"')
def db_delete(context, text, table):
    if table == "restaurants":
        entry = context.db.session.query(Restaurant).filter_by(name=text)
    elif table == "dishes":
        entry = context.db.session.query(Dish).filter_by(name=text)
    else:
        entry = context.db.session.query(User).filter_by(name=text)
    assert entry.first() is not None
    entry.delete()
    context.db.session.commit()


@when(u'we update "{text}" in "{table}" with "{text_update}"')
def db_update(context, text, text_update, table):
    if table == "restaurants":
        entry = context.db.session.query(Restaurant).filter_by(name=text)
    elif table == "dishes":
        entry = context.db.session.query(Dish).filter_by(name=text)
    else:
        entry = context.db.session.query(User).filter_by(name=text)
    entry.first().name = text_update
    context.db.session.commit()


@then(u'we should see "{text}" in "{table}"')
def db_add_check(context, text, table):
    if table == "restaurants":
        assert context.db.session.query(Restaurant).filter_by(name=text).first() is not None
    elif table == "dishes":
        assert context.db.session.query(Dish).filter_by(name=text).first() is not None
    else:
        assert context.db.session.query(User).filter_by(name=text).first() is not None


@then(u'we should not see "{text}" in "{table}"')
def db_delete_check(context, text, table):
    if table == "restaurants":
        assert context.db.session.query(Restaurant).filter_by(name=text).first() is None
    elif table == "dishes":
        assert context.db.session.query(Dish).filter_by(name=text).first() is None
    else:
        assert context.db.session.query(User).filter_by(name=text).first() is None


@then(u'we should see "{value}" as the "{column}" of "{table}" "{id}"')
def db_check_value(context, value, column, table, id):
    if table == "restaurants":
        entry = rowtodict(Restaurant.query.filter_by(id=id).first())
        assert entry[column] == value
    elif table == "dishes":
        entry = rowtodict(Dish.query.filter_by(id=id).first())
        assert entry[column] == value
    else:
        entry = rowtodict(User.query.filter_by(id=id).first())
        assert entry[column] == value
