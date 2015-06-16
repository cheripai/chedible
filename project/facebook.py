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


from flask import Flask, render_template, redirect, url_for, request, flash, session, g
import json
from project import app
from project.schema import Restaurant, Dish, User
from rauth.service import OAuth2Service

app.config.update(
    FACEBOOK_CLIENT_ID='1659176284311034',
    FACEBOOK_CLIENT_SECRET ='81219aaf2059e1ebd760bdb1fb0387a1',
)


facebook = OAuth2Service(
    name='facebook',
    client_id=app.config['FACEBOOK_CLIENT_ID'],
    client_secret=app.config['FACEBOOK_CLIENT_SECRET'],
    authorize_url='https://graph.facebook.com/oauth/authorize',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    base_url='https://graph.facebook.com/')

@app.route('/facebook/login')
def facebook_login():
    # Stores URL of page user was on last
    # This allows them to resume where they left off
    global USER_RETURN_URL
    if request.host_url in request.referrer:
        USER_RETURN_URL = request.referrer
    else:
        USER_RETURN_URL = request.host_url

    redirect_uri = url_for('facebook_authorized', _external=True)
    params = {
        'client-id': app.config['FACEBOOK_CLIENT_ID'],
        'redirect_uri': redirect_uri,
        'scope': 'email'
    }
    return redirect(facebook.get_authorize_url(**params))


@app.route('/facebook/authorized')
def facebook_authorized():
    if not 'code' in request.args:
        flash('You did not authorize the request')
        return redirect(USER_RETURN_URL)

    redirect_uri = url_for('facebook_authorized', _external=True)
    data = dict(code=request.args['code'], redirect_uri=redirect_uri)

    user_session = facebook.get_auth_session(data=data)

    me = user_session.get('me').json()

    picture_url = 'https://graph.facebook.com/' + me['id'] + '/picture'


    if me['name']:
        user = User.get_or_create(me['name'], me['id'], picture_url, me['email'])
    else:
        user = User.get_or_create(me['email'], me['id'], picture_url, me['email'])
    
    if not user.is_banned:
        session['logged_in'] = True
        session['user_id'] = user.id
        flash('Logged in as {}'.format(user.name))
    else:
        flash('Cannot log in with a banned account')
    
    return redirect(USER_RETURN_URL)
