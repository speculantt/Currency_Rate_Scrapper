from crypto_data import import_crypto_data, map_token_ids
from db_publisher import get_crypto_from_json, crypto_data_db_write
from currencies import currency_import_write

if __name__ == '__main__':
    # map_token_ids()  # Gets token ids for using instead of names
    import_crypto_data()  # Gets crypto rates and writes them into JSON file
    actual_data = get_crypto_from_json()  # Reads crypto data from JSON
    crypto_data_db_write(actual_data)  # Writes CRYPTO data to the DB
    currency_import_write()  # Gets currency data and writes it to the DB
