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


from flask import Flask, render_template 
from project import app, db
from project.schema import Restaurant, Dish, User


@app.route('/')
def main():
    return render_template('index.html', )


@app.route('/search/<table>/<query>')
def display_db(table, query):
    message = "No entries found"

    if table == "dishes":
        data = db.session.query(Dish).filter(Dish.name.contains(query))
    elif table == "restaurants":
        data = db.session.query(Restaurant).filter(Restaurant.name.contains(query))
    elif table == "users":
        data = db.session.query(User).filter(User.name.contains(query))
    else:
        return render_template('search.html', message=message)

    if data.first() is not None:
        message = ""

    return render_template('search.html', message=message, data=data)
