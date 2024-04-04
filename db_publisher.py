import pyodbc
import json
import numpy as np
from config import server, database, db_user, db_password
from main import json_filename, token_list

token_list = token_list.split(',')


def get_data():
    # Extract data from the saved file and assign the values to the variables

    with open(json_filename, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

        for i in token_list:
            try:
                line_data = np.array([
                    json_data['data'][f'{i}']['id'],
                    json_data['data'][f'{i}']['symbol'],
                    json_data['data'][f'{i}']['name'],
                    json_data['data'][f'{i}']['quote']['EUR']['price'],
                    json_data['data'][f'{i}']['quote']['EUR']['last_updated'],
                    json_data['data'][f'{i}']['quote']['EUR']['percent_change_24h'],
                    json_data['data'][f'{i}']['quote']['EUR']['percent_change_7d'],
                    json_data['data'][f'{i}']['quote']['EUR']['percent_change_30d']
                ])
                matrix_data = np.vstack((matrix_data, line_data))
            except:
                matrix_data = np.array([
                    json_data['data'][f'{i}']['id'],
                    json_data['data'][f'{i}']['symbol'],
                    json_data['data'][f'{i}']['name'],
                    json_data['data'][f'{i}']['quote']['EUR']['price'],
                    json_data['data'][f'{i}']['quote']['EUR']['last_updated'],
                    json_data['data'][f'{i}']['quote']['EUR']['percent_change_24h'],
                    json_data['data'][f'{i}']['quote']['EUR']['percent_change_7d'],
                    json_data['data'][f'{i}']['quote']['EUR']['percent_change_30d']
                ])
    return matrix_data


def db_write(actual_data):
    conn = pyodbc.connect(Driver='{SQL Server}',
                          Server=server,
                          Database=database,
                          UID=db_user,
                          PWD=db_password)

    cursor = conn.cursor()
    print('Database connected successfully')

    for j in range(actual_data.shape[0]):

        # Check if the data exists already
        check_query = """SELECT COUNT (*) FROM [Financials].[dbo].[Currency_rates]
        WHERE [token_id] = ? and [Date] = ?"""
        check_query_params = [(actual_data[j, 0], actual_data[j, 4])]
        print('Checking token id ' + actual_data[j, 0] + ', updated on ' + actual_data[j, 4])
        cursor.executemany(check_query, check_query_params)

        records_num = int(cursor.fetchone()[0])
        if records_num > 0:
            print('Record already exists in the table - ' + str(records_num))

        elif records_num == 0:
            print('Record to be added to the database.')

            # Writing the new data
            query = """ INSERT INTO [Financials].[dbo].[Currency_rates] (
                    [Date], [Currency_code], [Currency], [Rate], [Updated], [Comment], [token_id], [percent_change_24h],
                    [percent_change_7d], [percent_change_30d], [Record_added]) 
                    values (?,?,?,?,?,null,?,?,?,?,GETDATE())           
                """

            params = [(actual_data[j, 4], actual_data[j, 1], actual_data[j, 2], actual_data[j, 3],
                       actual_data[j, 4], actual_data[j, 0], actual_data[j, 5], actual_data[j, 6],
                       actual_data[j, 7])]

            cursor.executemany(query, params)
            conn.commit()

    cursor.close()
    conn.close()
    print('Connection closed')


if __name__ == '__main__':
    actual_data = get_data()
    db_write(actual_data)
