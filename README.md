**Overview**

  This code reads crypto currency data from https://coinmarketcap.com/ using the API provided by the service.
  You should use your own API key stored in the config file. It is only needed to have Basic plan (free) for this code to run.

**Modules**

  _mapping module_ - Mapping request is to obtain IDs of the tokens, it is recommended to operate IDs, not the symbols, as there are several tokens with the same symbol.
  
  _get_data_ - Extracts the data from API based on the lists of token IDs requested. Stores this data into a JSON file.

  _parameters_ - Extracts values from JSON file saved on the previous step, assignes values to the variables.
