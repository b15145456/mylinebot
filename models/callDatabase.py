import psycopg2
import os

DATABASE_URL = os.environ['DATABASE_URL']

# CREATE QUERY
def initTable():
    creat_query = '''
            CREATE TABLE id_table(
            line_id CHARACTER (33) PRIMARY KEY,
            clinic Integer NOT NULL,
            number Integer NOT NULL
            );
            CREATE TABLE clinic_table(
            clinic Integer PRIMARY KEY,
            number Integer NOT NULL
            )'''
    sql(creat_query)

# INSERT QUERY
def addLineId(id, clinic, num):
    table_columns = '(line_id, clinic, number)'
    insert_query = f"""INSERT INTO id_table {table_columns} VALUES ('{id}', {clinic}, {num});"""
    sql(insert_query)

def addClinicNum(clinic, num):
    table_columns = '(clinic, number)'
    insert_query = f"""INSERT INTO clinic_table {table_columns} VALUES ({clinic}, {num});"""
    sql(insert_query)

# UPDATE QUERY
def updateLineNum(id, num):
    update_query = f"""UPDATE id_table SET number = {num} WHERE line_id = '{id}'"""
    sql(update_query)

def updateLineClinic(id, clinic):
    update_query = f"""UPDATE id_table SET clinic = {clinic} WHERE line_id = '{id}'"""
    sql(update_query)

def updateClinicNum(clinic, num):
    update_query = f"""UPDATE clinic_table SET number = {num} WHERE clinic = {clinic}"""
    sql(update_query)

# SELECT QUERY
def getClinicNum(clinic):
    select_query = f"""SELECT number FROM clinic_table WHERE clinic = {clinic}"""
    callDB = sql(select_query)
    return callDB()

def getIdNum(id):
    select_query = f"""SELECT * FROM id_table WHERE line_id = '{id}'"""
    callDB = sql(select_query)
    return callDB()

def getIdList():
    select_query = """SELECT * FROM id_table ORDER BY number"""
    callDB = sql(select_query)
    return callDB()

def getIdListFromClinic(clinic):
    select_query = f"""SELECT line_id, number FROM id_table WHERE clinic = {clinic} ORDER BY number"""
    callDB = sql(select_query)
    return callDB()

# DELETE QUERY
def deleteIdUseNum(num):
    delete_query = f"""DELETE FROM id_table WHERE number = {num}"""
    sql(delete_query)

def deleteIdUseId(id):
    delete_query = f"""DELETE FROM id_table WHERE line_id = '{id}'"""
    sql(delete_query)

def sql(query):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    cursor.execute(query)
    conn.commit()

    print(f"sql query''' {query} '''successfully")
    
    try:
        data = cursor.fetchall()
    except:
        data = [("no results to fetch")]
    
    cursor.close()
    conn.close()
    
    def getData():
        if data:
            return data
        else:
            return False
    
    return getData