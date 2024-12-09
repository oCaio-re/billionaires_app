import sqlite3

from flask import Flask,render_template, request
from app import app
import db

def sqlite_security(conn):
    #? Disable untruted schema modifications
    conn.execute("PRAGMA trusted_schema = OFF;")
    #? More integrity checks
    conn.execute("PRAGMA cell_size_check = ON;")
    #? Enforce referential integrity
    conn.execute("PRAGMA foreign_keys = ON;")

def get_db():
    conn = sqlite3.connect('DB/Billionaires.db')
    sqlite_security(conn)
    return conn

@app.route('/')
def home():  # put application's code here
    conn = get_db()
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

@app.route('/subject/<subject>')
def get_subject(subject):
    conn = get_db()
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
        ''', (current[7] + 1 if current[7] < 2591 else None,)).fetchall()
    prev = conn.execute(
        '''
        SELECT FULL_NAME
        FROM BILLIONAIRES 
        WHERE ID = ?
        ;
        ''', (current[7] - 1 if current[7] > 1 else None,)).fetchall()
    conn.commit()
    conn.close()
    return render_template('subject/subject.html', current=current, previous=prev, next=next)

@app.route('/top10')
def top10():
    conn = get_db()
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
    conn = get_db()
    # using prepared statement to avoid sql injection: https://en.wikipedia.org/wiki/SQL_injection#Root_causes
    top10_countries = conn.execute(
        f" SELECT b.POSITION, b.FULL_NAME, b.WEALTH / 1000, c.NAME, b.SOURCE "
        f" FROM BILLIONAIRES b JOIN COUNTRIES c "
        f" ON b.ID_CITIZENSHIP = c.ID "
        f" WHERE c.NAME like '%{input}%' "
        f" ORDER BY WEALTH DESC  "
        f" LIMIT 10;").fetchall()
    conn.commit()
    conn.close()
    return render_template('top10/top10-queries.html', top10_countries=top10_countries, input=input)


@app.route('/top10/q2/<input>')
def get_top10_by_industry(input):
    conn = get_db()
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
    conn = get_db()   
     # using prepared statement to avoid sql injection: https://en.wikipedia.org/wiki/SQL_injection#Root_causes
    top10_age = conn.execute(
        f" SELECT b.POSITION, b.FULL_NAME, b.WEALTH / 1000, c.NAME, b.SOURCE, i.industry, b.AGE "
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
    conn = get_db() 
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


@app.route('/all-list/q1/<input>')  # list all by asc age
def get_all_list_age(input):
    conn = get_db() 
    # using prepared statement to avoid sql injection: https://en.wikipedia.org/wiki/SQL_injection#Root_causes
    all_rank_age = conn.execute(
        f" SELECT b.POSITION, b.FULL_NAME, b.WEALTH, c.NAME, b.SOURCE, b.AGE "
        f" FROM BILLIONAIRES b JOIN COUNTRIES c "
        f" ON b.ID_CITIZENSHIP = c.ID "
        f" ORDER BY b.AGE {input} ;"
        , ).fetchall()
    conn.commit()
    conn.close()
    return render_template('all_list/all_list_asc_age.html', all_rank_age=all_rank_age, input=input)

@app.route('/all-list/q2/<input>') 
def get_all_list_last_name(input):
    conn = get_db()
    cursor = conn.cursor()
    input = input.capitalize()

    query = """
    SELECT b.FULL_NAME, b.AGE, b.WEALTH / 1000 AS WEALTH_IN_BILLIONS, c.NAME AS COUNTRY, b.SOURCE
    FROM BILLIONAIRES b
    JOIN COUNTRIES c ON b.ID_CITIZENSHIP = c.ID
    WHERE b.LAST_NAME = ?
    ORDER BY b.FULL_NAME;   
    """
    cursor.execute(query, (input,))
    results = cursor.fetchall()
    
    if not results:
        return render_template('erro.html', input=input)
        
    return render_template('all_list/all_list_by_last_name.html', input=input, all_rank_last_name=results)


@app.route('/all-list/q3/<input>')  # get top ty BY COUNTRY
def get_all_list_wealth(input):
    conn = get_db() 
    min_wealth = int(input)
    # using prepared statement to avoid sql injection: https://en.wikipedia.org/wiki/SQL_injection#Root_causes
    all_rank_wealth = conn.execute(
        '''
        SELECT b.POSITION, b.FULL_NAME, b.WEALTH, c.NAME, b.SOURCE 
        FROM BILLIONAIRES b JOIN COUNTRIES c
        ON b.ID_CITIZENSHIP = c.ID
        WHERE b.WEALTH / 1000 > ?
        ORDER BY b.WEALTH ASC 
        ;
        '''
        , (min_wealth,)).fetchall()
    conn.commit()
    conn.close()
    return render_template('all_list/all_list_wealth.html', all_rank_wealth=all_rank_wealth, input=input)

@app.route('/countries')
def get_countries():
    conn = get_db() 
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
        GROUP BY c.NAME
        ''').fetchall()
    conn.commit()
    conn.close()
    return render_template('countries/countries.html', countries=countries, countr_and_bill=countr_and_bill)

@app.route('/countries/q1/<input>')
def get_how_great(input):
    conn = get_db() 
    cursor = conn.cursor()
    input = input.title()
    query = """
    SELECT b.FULL_NAME, b.WEALTH / 1000 AS BILLIONAIRE_WEALTH, c.NAME AS COUNTRY, c.GDP / c.POPULATION AS AVERAGE_CITIZEN_WEALTH
    FROM BILLIONAIRES b
    JOIN COUNTRIES c ON b.ID_CITIZENSHIP = c.ID
    WHERE b.FULL_NAME LIKE ? 
    """

    cursor.execute(query, ('%' + input + '%',))
    q1_how_great = cursor.fetchall()

    if not q1_how_great:
        return render_template('erro.html', input=input)
    
    return render_template('countries/countries_wealth.html', q1_how_great=q1_how_great, input=input)

@app.route('/countries/q2/<input>')
def get_years_left(input):
    conn = get_db() 
    cursor = conn.cursor()
    input = input.capitalize()

    query = """
    SELECT b.POSITION, b.FULL_NAME, b.WEALTH / 1000 AS BILLIONAIRE_WEALTH, b.SOURCE, b.AGE
    FROM BILLIONAIRES b
    JOIN COUNTRIES c ON b.ID_CITIZENSHIP = c.ID
    WHERE c.NAME LIKE ?
    ORDER BY b.POSITION ASC
    """

    cursor.execute(query, (input,))
    q2_born_at = cursor.fetchall()

    if not q2_born_at:
        return render_template('erro.html', input=input)
    
    return render_template('countries/countries_born_amount.html', input=input, q2_born_at=q2_born_at)

@app.route('/countries/q3/<input>')
def get_born_at(input):
    conn = get_db() 
    cursor = conn.cursor()
    input = input.title()

    query = """
    SELECT b.FULL_NAME, b.AGE, 100 - b.AGE AS YEARS_LEFT, b.WEALTH / 1000 AS BILLIONAIRE_WEALTH, b.SOURCE
    FROM BILLIONAIRES b
    WHERE b.FULL_NAME LIKE ?
    """

    cursor.execute(query, (f'%{input}%',))
    q3_years_left = cursor.fetchall()

    if not q3_years_left:
        return render_template('erro.html', input=input)
    
    return render_template('countries/countries_years_left.html', input=input, q3_years_left=q3_years_left)

@app.route('/industries')
def all_list():
    conn = get_db() 
    industries_list = conn.execute(
        '''
        SELECT * 
        FROM INDUSTRIES 
        ORDER BY ID ;
        '''
        , ).fetchall()
    conn.commit()
    conn.close()
    return render_template('industries/industries.html', industries_list=industries_list)


@app.route('/industries/q1/<input>')
def industries_specific_bil(input):
    conn = get_db() 
    bil_per_ind = conn.execute(
        '''
        SELECT b.POSITION, b.FULL_NAME, b.WEALTH,  b.SOURCE, i.industry
        FROM BILLIONAIRES b JOIN INDUSTRIES i
        ON b.id_industry = i.ID
        WHERE i.industry LIKE CONCAT('%', ? , '%')
        ORDER BY b.WEALTH DESC;
        '''
        , (input,)).fetchall()
    conn.commit()
    conn.close()
    return render_template('industries/industries_specific_bil.html', bil_per_ind=bil_per_ind, input=input)


@app.route('/industries/q2/<input>')
def industries_amount_of_bil(input):
    conn = get_db() 
    target = int(input)
    amount_of_bil = conn.execute(
        '''
            SELECT i.INDUSTRY, COUNT(b.position) AS billionaire_count
            FROM BILLIONAIRES b JOIN INDUSTRIES i
            ON b.id_industry = i.id
            GROUP BY i.INDUSTRY
            HAVING billionaire_count > ?
            ORDER BY billionaire_count DESC
            ;
            '''
        , (target,)).fetchall()
    conn.commit()
    conn.close()
    return render_template('industries/industries_amount_of_bil.html', amount_of_bil=amount_of_bil, input=input)

@app.route('/industries/q3/<input>')
def wealth_per_ind(input):
    conn = get_db() 
    wealth_per_ind = conn.execute(
           f" SELECT i.INDUSTRY, SUM(b.WEALTH) / 1000 AS TOTAL_WEALTH"
           f" FROM BILLIONAIRES b JOIN INDUSTRIES i"
           f" ON b.ID_INDUSTRY = i.ID"
           f" GROUP BY i.INDUSTRY"
           f" ORDER BY TOTAL_WEALTH {input}"
        , ).fetchall()
    conn.commit()
    conn.close()

    return render_template('industries/industries_wealth.html', wealth_per_ind=wealth_per_ind, input=input)
