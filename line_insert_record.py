import os
import psycopg2

def line_insert_record(record_list):
    DATABASE_URL = os.environ['DATABASE_URL']
    # DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a clinic-bot-v1').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    table_columns = '(alpaca_name, training, duration, date)'
    postgres_insert_query = f"""INSERT INTO alpaca_training {table_columns} VALUES (%s,%s,%s,%s)"""

    cursor.executemany(postgres_insert_query, record_list)
    conn.commit()

    message = f"恭喜您！ {cursor.rowcount} 筆資料成功匯入 alpaca_training 表單！success insert data!!"
    print(message)

    cursor.close()
    conn.close()
    
    return message
