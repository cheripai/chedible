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


from flask import Flask, render_template, redirect, url_for, request, flash, session
from functools import wraps
from project import app, db
from project.google import google
from project.schema import Restaurant, Dish, User
from sqlalchemy_searchable import search


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to be logged in to do that!')
            return redirect(url_for('main'))
    return wrap


@app.route('/')
def main():
    try:
        session['logged_in']
        user = User.query.filter_by(auth_id=session['user_id']).first()
        print(user)
        return render_template('index.html', user=user)
    except KeyError:
        return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    flash('Logged out')
    session.pop('logged_in', None)
    return redirect(url_for('main'))


# Used to log in a test user
# Can only be accessed if the TESTING flag is true
@app.route('/test_login/<id>')
def test_login(id):
    if app.config['TESTING']:
        session['logged_in'] = True
        session['user_id'] = id
    return redirect(url_for('main'))


@app.route('/search', methods=['POST'])
def search():
    if request.form['query']:
        return redirect(url_for('search_results', table='restaurants', query=request.form['query']))
    else:
        return render_template('index.html')


@app.route('/search_results/<table>/<query>')
def search_results(table, query):
    message = "No entries found"
    MAX_QUERIES = 50

    # removes special characters from search to prevent errors
    stripped_query = ''.join(c for c in query if c.isalnum() or c == ' ')
    if stripped_query == '':
        return render_template('search.html', message=message, query=query)
        
    if table == "dishes":
        data = Dish.query.search(stripped_query).limit(MAX_QUERIES)
    elif table == "restaurants":
        data = Restaurant.query.search(stripped_query).limit(MAX_QUERIES)
    elif table == "users":
        data = User.query.search(stripped_query).limit(MAX_QUERIES)
    else:
        return render_template('search.html', message=message)

    if data.first() is not None:
        message = ""

    return render_template('search.html', message=message, data=data, query=query)
