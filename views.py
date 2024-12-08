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


@app.route('/top10/q1/<input>')  # get top ty BY COUNTRY
def get_top10_by_country(input):
    conn = sqlite3.connect('DB/Billionaires.db')
    # using prepared statement to avoid sql injection: https://en.wikipedia.org/wiki/SQL_injection#Root_causes
    top10_countries = conn.execute(
        f" SELECT b.POSITION, b.FULL_NAME, b.WEALTH / 1000, c.NAME, b.SOURCE " 
        f" FROM BILLIONAIRES b JOIN COUNTRIES c "
        f" ON b.ID_CITIZENSHIP = c.ID " 
        f" WHERE c.NAME like '%{input}%' "
        f" ORDER BY WEALTH DESC  "
        f" LIMIT 10;" ).fetchall()
    conn.commit()
    conn.close()
    return render_template('top10/top10-queries.html', top10_countries=top10_countries, input=input)

@app.route('/top10/q2/<input>')
def get_top10_by_industry(input):
    conn = sqlite3.connect('DB/Billionaires.db')
    # using prepared statement to avoid sql injection: https://en.wikipedia.org/wiki/SQL_injection#Root_causes
    top10_industries = conn.execute(
       f" SELECT b.POSITION, b.FULL_NAME, b.WEALTH / 1000, c.NAME, b.SOURCE, i.industry "
       f" FROM BILLIONAIRES b JOIN COUNTRIES c JOIN INDUSTRIES i "
       f" ON b.ID_CITIZENSHIP = c.ID AND b.id_industry = i.ID "
       f" WHERE i.industry LIKE '%{input}%' "
       f" ORDER BY WEALTH DESC "
       f" LIMIT 10; "
            ).fetchall()

    conn.commit()
    conn.close()
    return render_template('top10/top10-industry.html', top10_industries=top10_industries, input=input)


@app.route('/top10/q3/<input>')
def get_top10_by_age(input):
    conn = sqlite3.connect('DB/Billionaires.db')
    # using prepared statement to avoid sql injection: https://en.wikipedia.org/wiki/SQL_injection#Root_causes
    top10_age = conn.execute(
       f" SELECT b.POSITION, b.FULL_NAME, b.WEALTH / 1000, c.NAME, b.SOURCE, i.industry "
       f" FROM BILLIONAIRES b JOIN COUNTRIES c JOIN INDUSTRIES i "
       f" ON b.ID_CITIZENSHIP = c.ID AND b.id_industry = i.ID "
       f" WHERE b.AGE = {int(input)} "
       f" ORDER BY WEALTH DESC "
       f" LIMIT 10; "
            ).fetchall()

    conn.commit()
    conn.close()
    return render_template('top10/top10-age.html', top10_age=top10_age, input=input)

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
    countr_and_bill = conn.execute(
        '''
        SELECT c.NAME, c.CONTINENT, c.TAX_RATE, c.POPULATION, c.LIFE_EXPECTANCY, c.GDP, b.POSITION, b.FULL_NAME, b.WEALTH
        FROM COUNTRIES c JOIN BILLIONAIRES b
        ON c.ID = b.ID_CITIZENSHIP 
        ''').fetchall()
    conn.commit()
    conn.close()
    return render_template('countries/countries.html', countries=countries, countr_and_bill=countr_and_bill)


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
