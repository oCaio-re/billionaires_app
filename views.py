from flask import Flask
from flask import render_template
from app import app


@app.route('/')
def home():  # put application's code here
    return render_template('home/home.html')


@app.route('/top10')
def top10():
    return render_template('top10/top10.html')

@app.route('/all_list')
def all_list():
    return 'CAUA'
