# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from behave import *
from flask import session
from project.schema import User

#using steps from chedible_steps.py:
#       @then(u'we should see the text "{text}"')
#       @then(u'we should not see the text "{text}"')

#using steps from database_steps.py
#       @when(u'we add "{text}" to "{table}"')


@when(u'we log in')
def login(context):
    user = User('test user', '', '', '')
    context.db.session.add(user)
    context.db.session.commit()
    context.page = context.client.get('/test_login/{}'.format(user.id), follow_redirects=True)


@when(u'we log out')
def logout(context):
    context.page = context.client.get('/logout', follow_redirects=True)
