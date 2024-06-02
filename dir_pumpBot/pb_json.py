########################################################################################################################
# ON MESSAGE # ON MESSAGE # ON MESSAGE # ON MESSAGE # ON MESSAGE # ON MESSAGE # ON MESSAGE # ON MESSAGE # ON MESSAGE # O
########################################################################################################################

# json: response
"""
{
    'e': 'kline',               # event type, in this case, it's "kline"
    'E': 1681113951171,         # event time, in milliseconds since the Unix epoch
    's': 'BTCUSDT',             # symbol, the trading pair for which this kline is for
    'k': {                      # kline data, contains the following parameters
        't': 1681113900000,     # kline start time, in milliseconds since the Unix epoch
        'T': 1681113959999,     # kline close time, in milliseconds since the Unix epoch
        's': 'BTCUSDT',         # symbol, the trading pair for which this kline is for
        'i': '1m',              # interval, the time interval for this kline (e.g., "1m" for 1 minute)
        'f': 3548801575,        # first trade ID
        'L': 3548802339,        # last trade ID
        'o': '28288.30',        # open price
        'c': '28288.40',        # close price
        'h': '28288.40',        # high price
        'l': '28286.20',        # low price
        'v': '51.230',          # volume
        'n': 765,               # number of trades
        'x': False,             # boolean, whether this kline is closed
        'q': '1449199.33690',   # quote asset volume
        'V': '27.902',          # taker buy base asset volume
        'Q': '789292.82860',    # taker buy quote asset volume
        'B': '0'                # ignore
    }
}
"""

########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
