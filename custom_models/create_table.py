import os
import psycopg2

DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a clinic-bot-v1').read()[:-1]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

create_table_query = '''CREATE TABLE alpaca_training(
    record_no serial PRIMARY KEY,
    alpaca_name VARCHAR (50) NOT NULL,
    training VARCHAR (50) NOT NULL,
    duration INTERVAL NOT NULL,
    date DATE NOT NULL
);'''

cursor.execute(create_table_query)
conn.commit()

cursor.close()
conn.close()