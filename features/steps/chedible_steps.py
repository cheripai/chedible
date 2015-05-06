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


@given(u'chedible is set up')
def flask_is_setup(context):
    assert context.client and context.db


@when(u'we visit the page')
def visit(context):
    context.page = context.client.get('/', follow_redirects=True)


@when(u'we add restaurant "{text}"')
def db_add(context, text):
    from project.schema import Restaurant
    restaurant = Restaurant(text, 'test', 'test')
    context.db.session.add(restaurant)


@then(u'we should see the text "{text}"')
def text(context, text):
    assert text in str(context.page.data)


@then(u'we should see "{text}" in restaurants')
def db_check(context, text):
    from project.schema import Restaurant
    assert text in str(context.db.session.query(Restaurant).first().name)
