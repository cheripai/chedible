# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from behave import *
from flask import g
import parse

from project import app
from project.schema import Restaurant, Dish, User
import project.chedible as chedible
import project.helpers as h

#using steps from database_steps.py
#       @when(u'we add "{text}" to "{table}"')


@given(u'chedible is set up')
def flask_is_setup(context):
    assert context.client and context.db


@when(u'we visit the page')
def visit(context):
    context.page = context.client.get('/', follow_redirects=True)


@when(u'we search "{table}" for "{text}"')
def search_restaurant(context, table, text):
    context.page = context.client.get('/search_results/{}/{}/0,0/0'.format(
        table, text))


@when(u'we visit "{route}"')
def visit_route(context, route):
    context.page = context.client.get(route, follow_redirects=True)


@when(
    u'we add restaurant "{text}" using the add restaurant page with tag "{tags}"'
)
def add_restaurant_using_add_restaurant_page(context, text, tags):
    context.page = context.client.post('/add',
                                       data=dict(name=text,
                                                 category='category',
                                                 tags=tags),
                                       follow_redirects=True)


@when(u'we add dish "{dish}" to restaurant "{restaurant}"')
def add_dish_using_add_dish_page(context, dish, restaurant):
    restaurant_id = context.db.session.query(Restaurant).filter_by(
        name=restaurant).first().id
    context.page = context.client.post(
        '/restaurant/{}/add'.format(restaurant_id),
        data=dict(name=dish,
                  price='0.00',
                  image='',
                  beef=True,
                  dairy=True,
                  egg=True,
                  fish=True,
                  gluten=True,
                  meat=True,
                  nut=True,
                  non_organic=True,
                  pork=True,
                  poultry=True,
                  shellfish=True,
                  soy=True,
                  wheat=True),
        follow_redirects=True)


@when(u'we edit restaurant "{old_name}" to "{new_name}"')
def edit_restaurant_using_edit_restaurant_page(context, old_name, new_name):
    restaurant_id = context.db.session.query(Restaurant).filter_by(
        name=old_name).first().id
    context.page = context.client.post(
        '/restaurant/{}/edit'.format(restaurant_id),
        data=dict(name=new_name,
                  category='category',
                  image='',
                  tags=''),
        follow_redirects=True)


@when(
    u'we edit dish "{old_name}" of restaurant "{restaurant}" to "{new_name}"')
def edit_dish_using_edit_dish_page(context, old_name, restaurant, new_name):
    restaurant_id = context.db.session.query(Restaurant).filter_by(
        name=restaurant).first().id
    dish_id = context.db.session.query(Dish).filter_by(
        name=old_name).first().id
    context.page = context.client.post('/restaurant/{}/{}/edit'.format(
        restaurant_id, dish_id),
                                       data=dict(name=new_name,
                                                 price='0.00',
                                                 image='',
                                                 beef=True,
                                                 dairy=True,
                                                 egg=True,
                                                 fish=True,
                                                 gluten=True,
                                                 meat=True,
                                                 nut=True,
                                                 non_organic=True,
                                                 pork=True,
                                                 poultry=True,
                                                 shellfish=True,
                                                 soy=True,
                                                 wheat=True),
                                       follow_redirects=True)


@then(u'we should see the text "{text}"')
def text(context, text):
    assert text in str(context.page.data)


@then(u'we should not see the text "{text}"')
def not_text(context, text):
    assert text not in str(context.page.data)


@then('is_chedible should evaluate to True given user "{user}" and "{dish}"')
def is_chedible_eval(context, user, dish):

    user_result = context.db.session.query(User).filter_by(name=user).first()
    dish_result = context.db.session.query(Dish).filter_by(name=dish).first()

    chedibility = h.is_chedible(dish_result, user_result)
    assert chedibility


@then('is_chedible should evaluate to False given user "{user}" and "{dish}"')
def is_chedible_eval(context, user, dish):

    user_result = context.db.session.query(User).filter_by(name=user).first()
    dish_result = context.db.session.query(Dish).filter_by(name=dish).first()

    chedibility = h.is_chedible(dish_result, user_result)
    assert not chedibility


@when(u'we disable testing')
def disable_testing(context):
    app.config['TESTING'] = False


@when(u'we enable testing')
def enable_testing(context):
    app.config['TESTING'] = True
