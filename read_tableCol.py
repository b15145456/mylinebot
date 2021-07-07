import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'alpaca_training'")
data = []
while True:
    temp = cursor.fetchone()
    if temp:
        data.append(temp)
    else:
        break
print(data)