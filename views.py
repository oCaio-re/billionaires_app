import sqlite3

from flask import Flask
from flask import render_template
from app import app
import db


@app.route('/')
def home():  # put application's code here
    conn = sqlite3.connect('database/billionaires')
    cursor = conn.cursor()
    top10 = conn.execute(
        '''
        SELECT b.POSITION, b.FULL_NAME, b.WEALTH, c.NAME, b.THE_SOURCE
        FROM BILLIONAIRES b JOIN COUNTRIES c
        ON b.CITIZENSHIP = c.NAME
        LIMIT 10
        ; 
        ''').fetchall()
    conn.commit()
    conn.close()
    return render_template('home/home.html', top10=top10)


@app.route('/top10')
def top10():
    conn = sqlite3.connect('database/billionaires')
    cursor = conn.cursor()
    top10 = conn.execute(
        '''
        SELECT b.POSITION, b.FULL_NAME, b.WEALTH, c.NAME, b.THE_SOURCE
        FROM BILLIONAIRES b JOIN COUNTRIES c
        ON b.CITIZENSHIP = c.NAME
        LIMIT 10
        ; 
        ''').fetchall()
    conn.commit()
    conn.close()
    return render_template('top10/top10.html', top10=top10)


@app.route('/top10/<country>')
def get_top10_by_country(country):
    conn = sqlite3.connect('database/billionaires')
    cursor = conn.cursor()
    top10 = conn.execute(
        f" SELECT b.POSITION, b.FULL_NAME, b.WEALTH, c.NAME, b.THE_SOURCE"
        f" FROM BILLIONAIRES b JOIN COUNTRIES c "
        f"ON b.CITIZENSHIP = c.NAME "
        f"WHERE c.NAME LIKE \'%{country}%\' "
        f"LIMIT 10;"
    ).fetchall()
    conn.commit()
    conn.close()
    return render_template('top10/top10-queries.html', top10=top10, country=country)


@app.route('/all_list')
def all_list():
    return 'CAUA'
