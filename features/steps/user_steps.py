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
from flask import session

#using steps from chedible_steps.py:
#       @then(u'we should see the text "{text}"')
#       @then(u'we should not see the text "{text}"')

#using steps from database_steps.py
#       @when(u'we add "{text}" to "{table}"')


@when(u'we log in with id "{id}"')
def login(context, id):
    context.page = context.client.get('/test_login/{}'.format(id), follow_redirects=True)


@when(u'we log out')
def logout(context):
    context.page = context.client.get('/logout', follow_redirects=True)
