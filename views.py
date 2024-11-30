from flask import Flask
from flask import render_template
from app import app


@app.route('/')
def home():  # put application's code here
    return render_template('home/home.html')


@app.route('/top10')
def top10():
    return 'Top10'
