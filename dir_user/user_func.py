########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# importing libraries
import os
import pickle

# importing dir: func
from dir_user.user_head import *


########################################################################################################################
# FILENAMES # FILENAMES # FILENAMES # FILENAMES # FILENAMES # FILENAMES # FILENAMES # FILENAMES # FILENAMES # FILENAMES
########################################################################################################################

# declaring filenames
FILENAME_CURRENT = 'dir_user/storage/user_current.txt'
FILENAME_PREVIOUS = 'dir_user/storage/user_previous.txt'


########################################################################################################################
# GET USER # GET USER # GET USER # GET USER # GET USER # GET USER # GET USER # GET USER # GET USER # GET USER # GET USER
########################################################################################################################

# function: getting global user
def get_user():
    global USER
    return USER


########################################################################################################################
# SET USER # SET USER # SET USER # SET USER # SET USER # SET USER # SET USER # SET USER # SET USER # SET USER # SET USER
########################################################################################################################

# function: setting user's chat id
def set_user(new_user):
    global USER
    USER = new_user


########################################################################################################################
# LOAD USER # LOAD USER # LOAD USER # LOAD USER # LOAD USER # LOAD USER # LOAD USER # LOAD USER # LOAD USER # LOAD USER
########################################################################################################################

# function: getting dir_user
def load_user():
    global USER
    if os.stat(FILENAME_CURRENT).st_size != 0:
        with open(FILENAME_CURRENT, 'rb') as f:
            old_user = pickle.load(f)
        return old_user
    else:
        return USER


########################################################################################################################
# USER SAVE # USER SAVE # USER SAVE # USER SAVE # USER SAVE # USER SAVE # USER SAVE # USER SAVE # USER SAVE # USER SAVE
########################################################################################################################

# function: saving all dir_user info
def save_user():
    global USER
    with open(FILENAME_CURRENT, 'wb') as f:
        pickle.dump(USER, f, protocol=pickle.HIGHEST_PROTOCOL)


########################################################################################################################
# DELETE USER # DELETE USER # DELETE USER # DELETE USER # DELETE USER # DELETE USER # DELETE USER # DELETE USER # DELETE
########################################################################################################################

# function: clearing dir_user info to user_current.txt + saving dir_user info to user_previous.txt
def delete_user():
    if os.stat(FILENAME_CURRENT).st_size != 0:
        with open(FILENAME_CURRENT, 'rb') as f:
            old_user = pickle.load(f)
        with open(FILENAME_PREVIOUS, 'wb') as f:
            pickle.dump(old_user, f, protocol=pickle.HIGHEST_PROTOCOL)

    # creating file
    os.remove(FILENAME_CURRENT)
    open(FILENAME_CURRENT, "w+")


########################################################################################################################
# GET DEFAULT USER # GET DEFAULT USER # GET DEFAULT USER # GET DEFAULT USER # GET DEFAULT USER # GET DEFAULT USER # GET
########################################################################################################################

# function: getting default user
def get_default_user():

    # declaring default fields
    token = ''
    password = ''
    user_id = 0
    chat_id = 0
    api_key = ''
    api_secret = ''
    quote_currency = 'USDT'

    # declaring bot settings
    bot_on_off = False
    assets_dict = dict()
    assets_tickers = list()
    trading_timeframes = set()
    wallet_empty_date = ''

    # filling user
    user = User(
        token=token,
        password=password,
        user_id=user_id,
        chat_id=chat_id,
        api_key=api_key,
        api_secret=api_secret,
        quote_currency=quote_currency,
        bot_on_off=bot_on_off,
        assets_dict=assets_dict,
        assets_tickers=assets_tickers,
        trading_timeframes=trading_timeframes,
        wallet_empty_date=wallet_empty_date
    )

    # return
    return user


########################################################################################################################
# USER CREATE # USER CREATE # USER CREATE # USER CREATE # USER CREATE # USER CREATE # USER CREATE # USER CREATE # USER C
########################################################################################################################

# creating USER
USER = get_default_user()


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
