import sqlite3
import pandas as pd

import datetime
import os

def excel_name():
    current_datetime = datetime.datetime.now()
    # print(current_datetime, type(current_datetime))
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    # print(formatted_datetime, type(formatted_datetime))
    formatted_datetime = formatted_datetime.replace(':', '-')
    # print(formatted_datetime)
    return formatted_datetime

def mkdir():
    directory_name = "downloads"

    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    else:
        pass

    return directory_name

def download_records():

    connection = sqlite3.connect(r'F:\ROTA\instance\mydatabase.db')
    cursor = connection.cursor()
    query = "SELECT name FROM sqlite_master WHERE type='table';"

    cursor.execute(query)

    tables = cursor.fetchall()

    table_names = [table[0] for table in tables]

    # print(table_names)

    sql_query = "SELECT * FROM admission_record"

    # Execute the query and fetch data into a DataFrame
    data = pd.read_sql(sql_query, connection)

    excel_file = mkdir()+os.sep+rf"{excel_name()}.xlsx"
    sheet_name = "Sheet1"

    # print(data)
    data.to_excel(excel_file, sheet_name=sheet_name, index=False)

    cursor.close()
    connection.close()

    return True

# download_records()
