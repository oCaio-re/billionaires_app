from datetime import datetime

import pandas as pd
import sqlite3

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', 1)

document = pd.ExcelFile('../Billionaires.xlsx')

sheet_names = document.sheet_names

df = pd.read_excel('../Billionaires.xlsx', sheet_names[0], dtype={'birth_date': 'string'})

column_industry = "industry"
column_data_industry = df[column_industry]
column_names = df.columns.tolist()
# print(column_names)

# for column in column_names:
#     for row in df[column]:
#         print(f"{column}: {row}")

# ------------------------------------ connecting to the DB --------------------------------------------
conn = sqlite3.connect('../DB/billionaires')
cursor = conn.cursor()

''' Inserting data on Industry table from the EXCEL (DONE ONCE, DON'T IT DO AGAIN!!!!) '''
# for i in billionaires_columns:
#     for e in df[i]:
# if type(e) == int:
#     cursor.execute(f"INSERT INTO BILLIONAIRES ({i}) VALUES ({e})", )
# else:
#     cursor.execute(f"INSERT INTO BILLIONAIRES ({i}) VALUES ('{e}')")


# print(type(e))
# print(f"{i}: {e}")
bill_column_names = "position, full_name, age, citizenship, gender, birth_date, last_name, wealth, industry, the_source, city_of_residence"
countries_column_names = "name, gdp_country, g_tertiary_ed_enroll, g_primary_ed_enroll, life_expectancy, tax_revenue, tax_rate, population, latitude, longitude, continent"
for row in df.itertuples(index=False):
    # cursor.execute(f"INSERT INTO Industry(name) VALUES (?) ON CONFLICT(name) DO NOTHING ", (row.industry, ))

    # cursor.execute(f"INSERT INTO Billionaires({bill_column_names}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ", (
    #     row.position, row.full_name, row.age, row.citizenship, row.gender, row.birth_date, row.last_name, row.wealth,
    #     row.industry, row.the_source, row.city_of_residence), )

    cursor.execute(f"INSERT INTO Countries({countries_column_names}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT(name) DO NOTHING", (
        row.country_of_residence, row.gdp_country, row.g_tertiary_ed_enroll, row.g_primary_ed_enroll, row.life_expectancy, row.tax_revenue, row.tax_rate, row.population, row.latitude,
        row.longitude, row.continent), )

INPUT1 = 'farofa'
    f"INSERT INTO BILLIONAIRES({INPUT1}) VALUES ({})"
    f"SELECT c.{ID}"
conn.commit()
conn.close()
