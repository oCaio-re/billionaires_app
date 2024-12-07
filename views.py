import sqlite3

from flask import Flask
from flask import render_template
from app import app
import db


@app.route('/')
def home():  # put application's code here
    conn = sqlite3.connect('DB/Billionaires.db')
    cursor = conn.cursor()
    top10 = conn.execute(
        '''
        SELECT b.POSITION, b.FULL_NAME, b.WEALTH, c.NAME, b.SOURCE
        FROM BILLIONAIRES b JOIN COUNTRIES c
        ON b.ID_CITIZENSHIP = c.ID
        LIMIT 10
        ; 
        ''').fetchall()
    conn.commit()
    conn.close()
    return render_template('home/home.html', top10=top10)


@app.route('/top10')
def top10():
    conn = sqlite3.connect('DB/Billionaires.db')
    cursor = conn.cursor()
    top10 = conn.execute(
        '''
        SELECT b.POSITION, b.FULL_NAME, b.WEALTH, c.NAME, b.SOURCE
        FROM BILLIONAIRES b JOIN COUNTRIES c
        ON b.ID_CITIZENSHIP = c.ID
        LIMIT 10
        ; 
        ''').fetchall()
    conn.commit()
    conn.close()
    return render_template('top10/top10.html', top10=top10)


@app.route('/top10/country/<country>')  # get top ty BY COUNTRY
def get_top10_by_country(country):
    conn = sqlite3.connect('DB/Billionaires.db')
    # using prepared statement to avoid sql injection: https://en.wikipedia.org/wiki/SQL_injection#Root_causes
    top10 = conn.execute(
        '''
        SELECT b.POSITION, b.FULL_NAME, b.WEALTH / 1000, c.NAME, b.SOURCE 
        FROM BILLIONAIRES b JOIN COUNTRIES c
        ON b.ID_CITIZENSHIP = c.ID 
        WHERE c.NAME = ? COLLATE NOCASE 
        ORDER BY WEALTH DESC 
        LIMIT 10;
        '''
        , (country,)).fetchall()
    conn.commit()
    conn.close()
    return render_template('top10/top10-queries.html', top10=top10, country=country)


@app.route('/all-list')  # get top ty BY COUNTRY
def get_all_list():
    conn = sqlite3.connect('DB/Billionaires.db')
    # using prepared statement to avoid sql injection: https://en.wikipedia.org/wiki/SQL_injection#Root_causes
    all_rank = conn.execute(
        '''
        SELECT b.POSITION, b.FULL_NAME, b.WEALTH, c.NAME, b.SOURCE 
        FROM BILLIONAIRES b JOIN COUNTRIES c
        ON b.ID_CITIZENSHIP = c.ID
        ;
        '''

        , ).fetchall()
    conn.commit()
    conn.close()
    return render_template('all_list/all_list.html', all_rank=all_rank)


@app.route('/countries')
def get_countries():
    conn = sqlite3.connect('DB/Billionaires.db')
    cursor = conn.cursor()
    countries = conn.execute(
        '''
        SELECT NAME, CONTINENT, TAX_RATE, POPULATION, LIFE_EXPECTANCY
        FROM COUNTRIES
        ;
        ''').fetchall()
    conn.commit()
    conn.close()
    return render_template('countries/countries.html', countries=countries)


@app.route('/subject/<subject>')
def get_subject(subject):
    conn = sqlite3.connect('DB/Billionaires.db')
    current = conn.execute(
        ' SELECT b.POSITION, b.FULL_NAME, b.GENDER, b.WEALTH / 1000, c.NAME, b.SOURCE, i.INDUSTRY, b.ID, b.GENDER, b.AGE, b.BIRTHDATE, b.CITY_OF_RESIDENCE, b.COUNTRY_OF_RESIDENCE, b.SOURCE  '
        ' FROM BILLIONAIRES b JOIN COUNTRIES c JOIN INDUSTRIES i '
        ' ON b.ID_CITIZENSHIP = c.ID AND b.ID_INDUSTRY = i.ID '
        ' WHERE b.FULL_NAME LIKE \'%' + subject + '%\'', ).fetchone()
    next = conn.execute(
        '''
        SELECT FULL_NAME
        FROM BILLIONAIRES 
        WHERE ID = ?
        ;
        ''', (current[7] + 1 if current[7] < 2591 else None, )).fetchall()
    prev = conn.execute(
        '''
        SELECT FULL_NAME
        FROM BILLIONAIRES 
        WHERE ID = ?
        ;
        ''', (current[7] - 1 if current[7] > 1 else None, )).fetchall()
    conn.commit()
    conn.close()
    return render_template('subject/subject.html', current=current, previous=prev, next=next)


@app.route('/all_list')
def all_list():
    return 'CAUA'
