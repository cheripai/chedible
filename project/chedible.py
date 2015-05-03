from flask import Flask, render_template 
from project import app, db
from project.schema import Restaurant, Dish


@app.route('/')
def main():
    return render_template('index.html', )


@app.route('/db/')
def display_db():
    data = db.session.query(Dish)
    return render_template('db.html', data=data)
