# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from behave import *
import parse

from project.helpers import rowtodict
from project.schema import Restaurant, Dish, User, Comment, Location, Issue
from time import time


@when(u'we add "{text}" to "{table}"')
def db_add(context, text, table):
    if table == "restaurants":
        entry = Restaurant(text, 'test', 'test', None)
    elif table == "dishes":
        entry = Dish(text, 0.00, None, None, None, None, None, None, None,
                     None, None, None, None, None, None, None, None)
    elif table == "users":
        entry = User(text, '', '', '')
    elif table == "comments":
        entry = Comment(None, None, text)
    elif table == "locations":
        entry = Location(None, '', 0.0, 0.0, text)
    elif table == "issues":
        entry = Issue(0, '', 0, text)
    context.db.session.add(entry)
    context.db.session.commit()


@when(u'we update "{text}" in "{table}" with "{text_update}"')
def db_update(context, text, text_update, table):
    if table == "restaurants":
        entry = context.db.session.query(Restaurant).filter_by(name=text)
        entry.first().name = text_update
    elif table == "dishes":
        entry = context.db.session.query(Dish).filter_by(name=text)
        entry.first().name = text_update
    elif table == "users":
        entry = context.db.session.query(User).filter_by(name=text)
        entry.first().name = text_update
    elif table == "comments":
        entry = context.db.session.query(Comment).filter_by(content=text)
        entry.first().content = text_update
    elif table == "locations":
        entry = context.db.session.query(Location).filter_by(address=text)
        entry.first().address = text_update
    elif table == "issues":
        entry = context.db.session.query(Issue).filter_by(content=text)
        entry.first().content = text_update
    context.db.session.commit()


@when(u'we delete "{text}" from "{table}"')
def db_delete(context, text, table):
    if table == "restaurants":
        entry = context.db.session.query(Restaurant).filter_by(name=text)
    elif table == "dishes":
        entry = context.db.session.query(Dish).filter_by(name=text)
    elif table == "users":
        entry = context.db.session.query(User).filter_by(name=text)
    elif table == "comments":
        entry = context.db.session.query(Comment).filter_by(content=text)
    elif table == "locations":
        entry = context.db.session.query(Location).filter_by(address=text)
    elif table == "issues":
        entry = context.db.session.query(Issue).filter_by(content=text)
    assert entry.first() is not None
    entry.delete()
    context.db.session.commit()


@when(u'we update the username "{username}" to user "{text}"')
def db_user_column_update(context, username, text):
    entry = context.db.session.query(User).filter_by(name=text)
    entry.first().username = username
    context.db.session.commit()


@when(
    u'we set all of user "{user}" preferences to "{boolean}" except for "{food}"'
)
def db_user_preferences_all(context, user, boolean, food):
    if boolean is "True":
        boolean = True
    elif boolean is "False":
        boolean = False

    entry = context.db.session.query(User).filter_by(name=user).first()
    entry.beef = boolean
    entry.dairy = boolean
    entry.egg = boolean
    entry.fish = boolean
    entry.gluten = boolean
    entry.meat = boolean
    entry.nut = boolean
    entry.non_organic = boolean
    entry.pork = boolean
    entry.poultry = boolean
    if food == "shellfish":
        entry.shellfish = not boolean
    else:
        entry.shellfish = boolean
    entry.soy = boolean
    entry.wheat = boolean

    context.db.session.commit()


@when(
    u'we set dish "{dish}" so contains is "{boolean}" for attribute/s "{food_attrs}"'
)
def db_dish_attributes_all(context, dish, boolean, food_attrs):
    if boolean is "True":
        boolean = True
    elif boolean is "False":
        boolean = False
    else:
        boolean = None

    entry = context.db.session.query(Dish).filter_by(name=dish).first()

    entry.beef = boolean
    entry.dairy = boolean
    entry.egg = boolean
    entry.fish = boolean
    entry.gluten = boolean
    entry.meat = boolean
    entry.nut = boolean
    entry.non_organic = boolean
    entry.pork = boolean
    entry.poultry = boolean
    entry.shellfish = boolean
    entry.soy = boolean
    entry.wheat = boolean

    context.db.session.commit()


@then(u'we should see "{text}" in "{table}"')
def db_add_check(context, text, table):
    if table == "restaurants":
        assert context.db.session.query(Restaurant).filter_by(
            name=text).first() is not None
    elif table == "dishes":
        assert context.db.session.query(Dish).filter_by(
            name=text).first() is not None
    elif table == "users":
        assert context.db.session.query(User).filter_by(
            name=text).first() is not None
    elif table == "comments":
        assert context.db.session.query(Comment).filter_by(
            content=text).first() is not None
    elif table == "locations":
        assert context.db.session.query(Location).filter_by(
            address=text).first() is not None
    elif table == "issues":
        assert context.db.session.query(Issue).filter_by(
            content=text).first() is not None


@then(u'we should not see "{text}" in "{table}"')
def db_delete_check(context, text, table):
    if table == "restaurants":
        assert context.db.session.query(Restaurant).filter_by(
            name=text).first() is None
    elif table == "dishes":
        assert context.db.session.query(Dish).filter_by(
            name=text).first() is None
    elif table == "users":
        assert context.db.session.query(User).filter_by(
            name=text).first() is None
    elif table == "comments":
        assert context.db.session.query(Comment).filter_by(
            content=text).first() is None
    elif table == "locations":
        assert context.db.session.query(Location).filter_by(
            address=text).first() is None
    elif table == "issues":
        assert context.db.session.query(Issue).filter_by(
            content=text).first() is None


@then(u'we should see "{value}" as the "{column}" of "{table}" "{id}"')
def db_check_value(context, value, column, table, id):
    if value == "time":
        value = str(int(time()))
    if table == "restaurants":
        entry = rowtodict(Restaurant.query.filter_by(id=id).first())
        assert str(entry[column]) == value
    elif table == "dishes":
        entry = rowtodict(Dish.query.filter_by(id=id).first())
        assert str(entry[column]) == value
    elif table == "users":
        entry = rowtodict(User.query.filter_by(id=id).first())
        assert str(entry[column]) == value
    elif table == "comments":
        entry = rowtodict(Comment.query.filter_by(id=id).first())
        assert str(entry[column]) == value
    elif table == "locations":
        entry = rowtodict(Location.query.filter_by(id=id).first())
        assert str(entry[column]) == value
    elif table == "issues":
        entry = rowtodict(Issue.query.filter_by(id=id).first())
        assert str(entry[column]) == value


@then(u'we should not see "{value}" as the "{column}" of "{table}" "{id}"')
def db_check_value(context, value, column, table, id):
    if table == "restaurants":
        entry = rowtodict(Restaurant.query.filter_by(id=id).first())
        assert str(entry[column]) != value
    elif table == "dishes":
        entry = rowtodict(Dish.query.filter_by(id=id).first())
        assert str(entry[column]) != value
    elif table == "users":
        entry = rowtodict(User.query.filter_by(id=id).first())
        assert str(entry[column]) != value
    elif table == "comments":
        entry = rowtodict(Comment.query.filter_by(id=id).first())
        assert str(entry[column]) != value
    elif table == "locations":
        entry = rowtodict(Location.query.filter_by(id=id).first())
        assert str(entry[column]) != value
    elif table == "issues":
        entry = rowtodict(Issue.query.filter_by(id=id).first())
        assert str(entry[column]) != value
