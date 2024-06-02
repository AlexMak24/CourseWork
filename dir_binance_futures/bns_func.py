########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# lib
import re
import requests


########################################################################################################################
# GET TRADE SYMBOLS # GET TRADE SYMBOLS # GET TRADE SYMBOLS # GET TRADE SYMBOLS # GET TRADE SYMBOLS # GET TRADE SYMBOLS
########################################################################################################################

# function: getting trading symbols on futures binance
def get_trade_symbols():
    url = 'http://fapi.binance.com/fapi/v1/ticker/24hr'
    res = requests.get(url).json()
    symbols = []
    for i in res:
        if re.search('.*USDT$', i['symbol']):
            symbols.append(i['symbol'].lower())
    return symbols


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
