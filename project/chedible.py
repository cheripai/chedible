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


from flask import Flask, render_template, redirect, url_for, request
from project import app, db
from project.schema import Restaurant, Dish, User
from sqlalchemy_searchable import search


@app.route('/')
def main():
    return render_template('index.html', )


@app.route('/search', methods=['POST'])
def search():
    return redirect(url_for('search_results', table='restaurants', query=request.form['query']))


@app.route('/search_results/<table>/<query>')
def search_results(table, query):
    message = "No entries found"
    MAX_QUERIES = 50

    if table == "dishes":
        data = Dish.query.search(query).limit(MAX_QUERIES)
    elif table == "restaurants":
        data = Restaurant.query.search(query).limit(MAX_QUERIES)
    elif table == "users":
        data = User.query.search(query).limit(MAX_QUERIES)
    else:
        return render_template('search.html', message=message)

    if data.first() is not None:
        message = ""

    return render_template('search.html', message=message, data=data)
