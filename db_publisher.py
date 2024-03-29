import pyodbc
import json
import numpy as np
from config import server, database, db_user, db_password
from main import json_filename, token_list

token_list = token_list.split(',')


def parameters():
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
        print(matrix_data)


def db_write():
    conn = pyodbc.connect(Driver='{SQL Server}',
                          Server=server,
                          Database=database,
                          UID=db_user,
                          PWD=db_password)

    cursor = conn.cursor()
    print('Database connected successfully')

    cursor.close()
    conn.close()
    print('Connection closed')


if __name__ == '__main__':
    parameters()
    # db_write()
