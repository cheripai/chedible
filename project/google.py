# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from flask import redirect, url_for, request, flash, session
from project import app
from project.schema import User
from rauth.service import OAuth2Service


USER_RETURN_URL = ""

app.config.update(
    GOOGLE_CLIENT_ID='114729784165-pf2ojuudj8gorq0gun8i2cv2prclm8lu.apps.googleusercontent.com',
    GOOGLE_CLIENT_SECRET='7f28wsnEAiOUa9GZHZLJCtTn',
)


google = OAuth2Service(
    name='google',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    base_url='https://www.googleapis.com/oauth2/v1/',
)


@app.route('/google/login')
def google_login():
    # Stores URL of page user was on last
    # This allows them to resume where they left off
    global USER_RETURN_URL
    if request.host_url in request.referrer:
        USER_RETURN_URL = request.referrer
    else:
        USER_RETURN_URL = request.host_url

    redirect_uri = url_for('google_authorized', _external=True)
    params = {
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'code',
        'redirect_uri': redirect_uri
    }
    return redirect(google.get_authorize_url(**params))


@app.route('/google/authorized')
def google_authorized():
    if 'code' not in request.args:
        flash('You did not authorize the request')
        return redirect(USER_RETURN_URL)

    redirect_uri = url_for('google_authorized', _external=True)
    data = dict(
        code=request.args['code'],
        redirect_uri=redirect_uri,
        grant_type='authorization_code'
    )

    response = google.get_raw_access_token(data=data)
    response = response.json()
    user_session = google.get_session(response['access_token'])

    json_path = 'https://www.googleapis.com/oauth2/v1/userinfo'
    me = user_session.get(json_path).json()

    if me['name']:
        user = User.get_or_create(
            me['name'],
            str(me['id']),
            me['picture'],
            me['email']
        )
    else:
        user = User.get_or_create(
            me['email'],
            str(me['id']),
            me['picture'],
            me['email']
        )

    if not user.is_banned:
        # Update user profile picture in case it may have changed
        User.query.filter_by(id=user.id).update({'image': me['picture']})
        session['logged_in'] = True
        session['user_id'] = user.id
        flash('Logged in as {}'.format(user.name))
    else:
        flash('Cannot log in with a banned account')

    return redirect(USER_RETURN_URL)
