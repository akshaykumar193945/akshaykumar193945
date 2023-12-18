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
    current_directory = os.getcwd()
    database_path = current_directory + os.sep + "instance" + os.sep + "mydatabase.db"
    connection = sqlite3.connect(database_path)

    cursor = connection.cursor()
    query = "SELECT name FROM sqlite_master WHERE type='table';"

    cursor.execute(query)

    tables = cursor.fetchall()

    table_names = [table[0] for table in tables]

    print(table_names)

    # sql_query_admission_record = "SELECT * FROM profiles"
    sql_query_user_record = "SELECT * FROM user_credentials"

    # Execute the queries and fetch data into DataFrames
    # profiles_data_df = pd.read_sql(sql_query_admission_record, connection)
    data_user_record = pd.read_sql(sql_query_user_record, connection)

    # print("Admission Record Data:")
    # print(data_admission_record)

    # print("User Record Data:")
    # print(data_user_record)

    excel_file = mkdir() + os.sep + rf"{excel_name()}.xlsx"

    # profiles_data = "Profile Data"
    user_record_data = "User Data"

    # Save data to different sheets in the Excel file
    # Create an Excel writer to save multiple DataFrames into the same Excel file
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        # profiles_data_df.to_excel(writer, sheet_name=profiles_data, index=False)
        data_user_record.to_excel(writer, sheet_name=user_record_data, index=False)

    cursor.close()
    connection.close()

    return True


# download_records()