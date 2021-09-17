import os
import psycopg2

def edit_number(change_num):
    DATABASE_URL = os.environ['DATABASE_URL']
    # DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a clinic-bot-v1').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
<<<<<<< HEAD
    data = str(change_num)
    table_columns = '(departments_id, number, edit_time)'
    postgres_insert_query = f"""UPDATE clinic_number SET departments_id=0, number={data}, edit_time=CURRENT_TIMESTAMP;"""

    cursor.executemany(postgres_insert_query, data)
=======
    data = change_num
    postgres_insert_query = f"""UPDATE clinic_number SET departments_id=0, number_now={data}, edit_time=CURRENT_TIMESTAMP;"""

    cursor.execute(postgres_insert_query)
>>>>>>> 48ea54759af8682a81b1a9f715f416b617286703
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
<<<<<<< HEAD
=======

def reset_number():
    DATABASE_URL = os.environ['DATABASE_URL']
    # DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a clinic-bot-v1').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    data = 0
    postgres_insert_query = f"""UPDATE clinic_number SET departments_id=0, number_now={data}, edit_time=CURRENT_TIMESTAMP;"""

    cursor.executemany(postgres_insert_query, data)
    conn.commit()

    message = f"恭喜您！ 成功修改資料"

    cursor.close()
    conn.close()
    
    return message

def get_tokenList():
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    postgres_select_query = f"""SELECT * FROM token_table ORDER BY number;"""
    
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


def exit_token(user_record):
    DATABASE_URL = os.environ['DATABASE_URL']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    
    postgres_select_query = f"""SELECT * FROM token_table WHERE token_id = '{user_record[0]}' ;"""
    
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
    if not message:
        return False
    else:
        return True
    


def insert_token(user_record):
    DATABASE_URL = os.environ['DATABASE_URL']
    # DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a clinic-bot-v1').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    table_columns = '(token_id, number)'
    postgres_insert_query = f"""INSERT INTO token_table {table_columns} VALUES (%s,%s)"""
    
    # INSERT INTO token_table ("token_id", "number") VALUES ('Uc20f5abc2ef473849e0958ba31a42044', '20')
    
    cursor.executemany(postgres_insert_query, [user_record])
    conn.commit()

    message = f"恭喜您！ {cursor.rowcount} 筆資料成功匯入 token_table 表單！success insert data!!"
    print(message)

    cursor.close()
    conn.close()
    
    return message

def change_token_data(user_record):
    DATABASE_URL = os.environ['DATABASE_URL']
    # DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a clinic-bot-v1').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    postgres_insert_query = f"""UPDATE token_table SET number={user_record[1]} WHERE token_id = '{user_record[0]}';"""

    cursor.execute(postgres_insert_query)
    conn.commit()

    message = f"恭喜您！ 成功修改資料"

    cursor.close()
    conn.close()
    
    return message

def del_token_data(now_num):
    DATABASE_URL = os.environ['DATABASE_URL']
    # DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a clinic-bot-v1').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    postgres_insert_query = f"""DELETE FROM token_table WHERE number = {now_num};"""

    cursor.execute(postgres_insert_query)
    conn.commit()

    message = f"恭喜您！成功刪除資料"

    cursor.close()
    conn.close()
    
    return message
>>>>>>> 48ea54759af8682a81b1a9f715f416b617286703
