from flask import Flask, render_template, redirect, url_for, request, flash, session
from project import app
from project.schema import Restaurant, Dish, User
from rauth.service import OAuth2Service


app.config.update(
    GOOGLE_CLIENT_ID='114729784165-pf2ojuudj8gorq0gun8i2cv2prclm8lu.apps.googleusercontent.com',
    GOOGLE_CLIENT_SECRET ='7f28wsnEAiOUa9GZHZLJCtTn',
)


google = OAuth2Service(
    name='google',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    client_id = app.config['GOOGLE_CLIENT_ID'],
    client_secret = app.config['GOOGLE_CLIENT_SECRET'],
    base_url='https://www.googleapis.com/oauth2/v1/',
)


@app.route('/google/login')
def google_login():
    redirect_uri = url_for('google_authorized', _external=True)
    params = {
        'scope': 'https://www.googleapis.com/auth/userinfo.email', 
        'response_type': 'code',
        'redirect_uri': redirect_uri
    }
    return redirect(google.get_authorize_url(**params))


@app.route('/google/authorized')
def google_authorized():
    if not 'code' in request.args:
        flash('You did not authorize the request')
        return redirect(url_for('main'))

    redirect_uri = url_for('google_authorized', _external=True)
    data = dict(code=request.args['code'], redirect_uri=redirect_uri, grant_type='authorization_code')

    response = google.get_raw_access_token(data=data)
    response = response.json()
    user_session = google.get_session(response['access_token'])

    json_path = 'https://www.googleapis.com/oauth2/v1/userinfo'
    me = user_session.get(json_path).json()
    User.get_or_create(me['name'], str(me['id']), me['picture'])
    
    session['logged_in'] = True
    session['user_id'] = me['id']
    
    flash('Logged in as {}'.format(me['name']))
    return redirect(url_for('main'))