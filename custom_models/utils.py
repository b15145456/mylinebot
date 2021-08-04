import os
import psycopg2

def edit_number(change_num):
    DATABASE_URL = os.environ['DATABASE_URL']
    # DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a clinic-bot-v1').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    data = change_num
    postgres_insert_query = f"""UPDATE clinic_number SET departments_id=0, now_number={data}, edit_time=CURRENT_TIMESTAMP;"""

    cursor.execute(postgres_insert_query)
    conn.commit()

    message = f"恭喜您！ 成功修改資料"

    cursor.close()
    conn.close()
    
    return message

def get_number():
    DATABASE_URL = os.environ['DATABASE_URL']
    # DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a clinic-bot-v1').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    postgres_select_query = f"""SELECT * FROM clinic_number;"""
    
    cursor.execute(postgres_select_query)
    
    message = []
    while True:
        temp = cursor.fetchmany(10)
        
        if temp:
            message.extend(temp)
        else:
            break
    
    cursor.close()
    conn.close()
    
    return message

def reset_number():
    DATABASE_URL = os.environ['DATABASE_URL']
    # DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a clinic-bot-v1').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    data = 0
    table_columns = '(departments_id, number, edit_time)'
    postgres_insert_query = f"""UPDATE clinic_number SET departments_id=0, now_number={data}, edit_time=CURRENT_TIMESTAMP;"""

    cursor.executemany(postgres_insert_query, data)
    conn.commit()

    message = f"恭喜您！ 成功修改資料"

    cursor.close()
    conn.close()
    
    return message