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
    context.page = context.client.get('/search_results/{}/{}'.format(table, text))


@when(u'we visit "{route}"')
def visit_route(context, route):
    context.page = context.client.get(route, follow_redirects=True)


@when(u'we add restaurant "{text}" using the add restaurant page')
def add_restaurant_using_add_restaurant_page(context, text):
    context.page = context.client.post('/add', data=dict(name=text, category='category', image=''), follow_redirects=True)


@then(u'we should see the text "{text}"')
def text(context, text):
    assert text in str(context.page.data)


@then(u'we should not see the text "{text}"')
def not_text(context, text):
    assert text not in str(context.page.data)
