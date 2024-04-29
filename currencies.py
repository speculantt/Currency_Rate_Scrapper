import requests
from bs4 import BeautifulSoup
import pyodbc
from config import server, database, db_user, db_password
from datetime import date

# USD input data
usd_datarowkey = 'FX_IDC:EURUSD'
usd_link = 'https://www.tradingview.com/markets/currencies/rates-major/'
# RUB input data
rub_datarowkey = 'FX_IDC:EURRUB'
rub_link = 'https://www.tradingview.com/markets/currencies/rates-exotic/'

params = [
    [usd_link, usd_datarowkey],
    [rub_link, rub_datarowkey]
]


def get_currency_rates(link, key):
    url = link
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        currency_table = soup.find('table', {'class': 'table-Ngq2xrcG'})
        if currency_table:
            # limiting data for EUR-RUB only
            rows = currency_table.find_all(attrs={"data-rowkey": key})
            currency_rates = []
            for row in rows:
                cells = row.find_all('td')

                currency_rates.append(cells[0].text.strip())  # currency_pair
                currency_rates.append(cells[1].text.strip())  # rate
                currency_rates.append(cells[2].text.strip())  # change

            return currency_rates
        else:
            print("Unable to find currency table on the page.")
    else:
        print("Failed to retrieve page:", response.status_code)


def db_write(currency_pair, rate, change):
    conn = pyodbc.connect(Driver='{SQL Server}',
                          Server=server,
                          Database=database,
                          UID=db_user,
                          PWD=db_password)

    cursor = conn.cursor()
    print('Database connected successfully.')

    # Check if the data exists already
    check_query = """SELECT COUNT (*) FROM [Financials].[dbo].[Currency_rates]
    WHERE [Currency_code] = ? and [Date] = ?"""
    check_query_params = [(currency_pair, str(date.today()))]
    print('Checking currency pair ' + currency_pair + ', updated on ' + str(date.today()))
    cursor.executemany(check_query, check_query_params)

    records_num = int(cursor.fetchone()[0])
    if records_num > 0:
        print('Record already exists in the table - ' + currency_pair + ' ' + str(date.today()))

    elif records_num == 0:
        print('Record to be added to the database.')

        try:
            # Writing the new data
            query = """ INSERT INTO [Financials].[dbo].[Currency_rates] (
                        [Date], [Currency_code], [Currency],[Rate],[Updated],[percent_change_24h],[Record_added]) 
                        values (?,?,?,?,?,?,?)           
                    """

            params = [(str(date.today()), currency_pair, currency_pair, rate, str(date.today()), change, str(date.today()))]
            cursor.executemany(query, params)
            conn.commit()
        except:
            print("Writing to DB failed.")

    cursor.close()
    conn.close()
    print('Connection closed')


if __name__ == "__main__":

    try:
        print("Latest Currency Rates:")
        for row in params:
            currency_rates = get_currency_rates(row[0], row[1])
            if currency_rates:
                currency_pair, rate, change = currency_rates  # assigning values to the array
                currency_pair = currency_pair[3:6]
                change = float(change.replace('%', ''))
                # print(currency_pair, rate, change)
                db_write(currency_pair, rate, change)
            else:
                print("Failed to fetch currency rates.")
    except:
        print("Failed to iterate through rates table.")
