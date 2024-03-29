from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from config import APIkey

json_crypto_filename = 'api_import_crypto.json'
json_fiat_filename = 'api_import_fiat.json'


def get_data():
    # Extract JSON values for the given coin IDs and store this data into a file
    # THIS IS PROD LINK - your API tokens will be spent
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters = {
        'id': '1,1027,11419,825,13502',
        'convert': 'EUR'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': APIkey,
    }
    '''
    ---LIST OF IDs---
    ID, Symbol, Name
    1       BTC    Bitcoin
    1027    ETH    Ethereum
    11419   TON    Toncoin
    825     USDT   Tether USDt
    13502   WLD    Worldcoin 
    --- FIAT ---
    2781    USD    United States Dollar
    2790    EUR    Euro 
	2806	RUB    Russian Ruble
    --- END ---
    '''
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        json_data = response.json()
        # Error handling
        if json_data['status']['error_code'] == 0:
            with open(json_crypto_filename, 'w', encoding='utf-8') as file:
                json.dump(json_data, file, indent=4)
            print('Hey, ', json_crypto_filename, ' file has been saved successfully.')
        else:
            print('Something is wrong. JSON file was not saved. Check this:')
            print(json_data['status']['error_message'])
    # Error handling
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def parameters():
    # Extract data from the saved file and assign the values to the variables

    with open(json_crypto_filename, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
        id_btc = json_data['data']['1']['id']
        symbol_btc = json_data['data']['1']['symbol']
        name_btc = json_data['data']['1']['name']
        price_btc = json_data['data']['1']['quote']['EUR']['price']
        print(id_btc, ' ', symbol_btc, ' ', name_btc, ' ', price_btc, 'EUR')


def mapping():
    # Map request is here to obtain IDs of the tokens, it is recommended to operate IDs, not the symbols
    # because there are several tokens with the same symbol

    # THIS IS PROD LINK - your API tokens will be spent
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'  # CRYPTO
    # url = 'https://pro-api.coinmarketcap.com/v1/fiat/map'   # FIAT
    parameters = {
        'symbol': 'BTC,ETH,TON,USDT,WLD',
        'listing_status': 'active'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': APIkey,
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        mapping_data = response.json()
        pretty_data = json.dumps(mapping_data, indent=4)
        print(pretty_data)
    # Error handling
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


if __name__ == '__main__':
    # mapping()
    get_data()
    # parameters()
