from flask import Flask, render_template 
from project import app, db

@app.route('/')
def main():
    return render_template('index.html')
