########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# importing libraries
from dataclasses import dataclass


########################################################################################################################
# USER # USER # USER # USER # USER # USER # USER # USER # USER # USER # USER # USER # USER # USER # USER # USER # USER #
########################################################################################################################

# User Class
@dataclass
class User:
    token: str                  # bot token
    password: str               # password
    user_id: float              # user id
    chat_id: float              # chat id
    api_key: str                # api key
    api_secret: str             # api secret
    quote_currency: str         # quote trading currency

    bot_on_off: bool            # bot on/off
    assets_dict: dict           # assets (ticker: data)
    assets_tickers: list        # assets ([tickers])
    trading_timeframes: set     # trading timeframes
    wallet_empty_date: str      # first date (empty wallet)


########################################################################################################################
# END ## END ## END ## END ## END ## END ## END ## END ### END ## END ## END ## END ## END ## END ## END ## END ## END #
########################################################################################################################
