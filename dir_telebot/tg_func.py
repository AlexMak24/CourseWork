########################################################################################################################
# IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT #
########################################################################################################################

# import libraries
import telebot
from telebot import types

# import global
from dir_telebot import tg_config as config
from dir_user.user_func import FILENAME_CURRENT

# import dir: msg
from dir_telebot.tg_msg import *

# import dir: func
from dir_pumpBot import pb_func as pb
from dir_user import user_func as usr


########################################################################################################################
# SESSION # SESSION # SESSION # SESSION # SESSION # SESSION # SESSION # SESSION # SESSION # SESSION # SESSION # SESSION
########################################################################################################################

# creating dir_telebot bot
TOKEN = config.choose_token()
BOT = telebot.TeleBot(TOKEN)


########################################################################################################################
# SEND USER # SEND USER # SEND USER # SEND USER # SEND USER # SEND USER # SEND USER # SEND USER # SEND USER # SEND USER
########################################################################################################################

# function: sending user.txt in telegram
def send_user_txt():
    user = usr.get_user()
    file_txt = open(FILENAME_CURRENT, 'rb')
    BOT.send_document(user.user_id, file_txt)


########################################################################################################################
# CHECK USER ID # CHECK USER ID # CHECK USER ID # CHECK USER ID # CHECK USER ID # CHECK USER ID # CHECK USER ID # CHECK
########################################################################################################################

# function: save/check user_id
def check_user_id(new_user_id, message):
    user = usr.get_user()
    user.chat_id = message.chat.id

    # user doesn't have user id
    if user.user_id == 0:
        old_user = usr.load_user()
        if old_user.user_id == new_user_id:
            session_request(message)

        # user had not a session
        else:
            usr.delete_user()
            user.user_id = new_user_id
            user.token = TOKEN
            BOT.send_message(message.chat.id, MSG_W_NEW)
            get_api_keys(message)

    # it is NOT OUR user
    else:
        if user.user_id != new_user_id:
            BOT.send_message(message.chat.id, MSG_M_PRIVATE_BOT)

        # it is OUR user
        elif user.user_id == new_user_id:
            return True


########################################################################################################################
# GET API KEYS # GET API KEYS # GET API KEYS # GET API KEYS # GET API KEYS # GET API KEYS # GET API KEYS # GET API KEYS
########################################################################################################################

# function: getting and saving api keys
def get_api_keys(message):
    msg = BOT.send_message(message.from_user.id, MSG_E_API_KEY)
    BOT.register_next_step_handler(msg, save_api_key)


# saving API Key
def save_api_key(message):
    user = usr.get_user()
    user.api_key = str(message.text)
    msg = BOT.send_message(message.from_user.id, MSG_E_API_SECRET)
    BOT.register_next_step_handler(msg, save_api_secret)


# saving API Secret
def save_api_secret(message):
    user = usr.get_user()
    user.api_secret = str(message.text)
    BOT.send_message(message.chat.id, MSG_S_KEYS)

    # setting new password
    msg = BOT.send_message(message.from_user.id, MSG_E_PASS)
    BOT.register_next_step_handler(msg, set_password)


########################################################################################################################
# SET PASSWORD # SET PASSWORD # SET PASSWORD # SET PASSWORD # SET PASSWORD # SET PASSWORD # SET PASSWORD # SET PASSWORD
########################################################################################################################

# function: setting new password
def set_password(message):
    user = usr.get_user()
    user.password = str(message.text)
    msg = BOT.send_message(message.from_user.id, MSG_E_PASS_AGAIN)
    BOT.register_next_step_handler(msg, set_password_again)


# function: setting new password
def set_password_again(message):
    user = usr.get_user()

    # passwords MATCH
    if user.password == str(message.text):
        BOT.send_message(message.chat.id, MSG_SAVED_PASS)
        usr.save_user()
        send_user_txt()

        # start main loop
        pb.start_threads()

    # passwords NOT MATCH
    else:
        user.password = ''
        BOT.send_message(message.chat.id, MSG_M_PASS_MISMATCH)
        msg = BOT.send_message(message.from_user.id, MSG_E_PASS)
        BOT.register_next_step_handler(msg, set_password)


########################################################################################################################
# CHECK PASSWORD # CHECK PASSWORD # CHECK PASSWORD # CHECK PASSWORD # CHECK PASSWORD # CHECK PASSWORD # CHECK PASSWORD #
########################################################################################################################

# function: checking password
def check_password(message):
    user = usr.get_user()
    if user.password == str(message.text):
        return True
    else:
        BOT.send_message(message.chat.id, MSG_M_PASS_WRONG)
        return False


########################################################################################################################
# ASK SESSION # ASK SESSION # ASK SESSION # ASK SESSION # ASK SESSION # ASK SESSION # ASK SESSION # ASK SESSION # ASK SE
########################################################################################################################

# function: continue session
def session_request(message):

    # creating buttons
    markup_inline = types.InlineKeyboardMarkup()
    item_old = types.InlineKeyboardButton(text='OLD', callback_data='old')
    item_new = types.InlineKeyboardButton(text='NEW', callback_data='new')

    # sending session question message
    markup_inline.add(item_old, item_new)
    BOT.send_message(message.chat.id, MSG_A_SESSION, reply_markup=markup_inline)


# callback: pushed button
@BOT.callback_query_handler(func=lambda call: (call.data == 'old') or (call.data == 'new'))
def session_response(answer):
    user = usr.get_user()

    # continue
    if str(answer.data) == "old":
        session_check_password_request(answer)

    # new one
    elif str(answer.data) == "new":
        usr.delete_user()
        user.user_id = answer.from_user.id
        user.token = TOKEN
        BOT.send_message(answer.from_user.id, MSG_W_NEW)
        get_api_keys(answer)


# function: password (request)
def session_check_password_request(answer):
    msg = BOT.send_message(answer.from_user.id, MSG_E_PASS)
    BOT.register_next_step_handler(msg, session_check_password_response)


# function: password (response)
def session_check_password_response(message):
    old_user = usr.load_user()

    # password is correct
    if old_user.password == str(message.text):
        usr.set_user(usr.load_user())
        BOT.send_message(message.chat.id, MSG_W_OLD)

        # start main loop
        pb.start_threads()

    # password is not correct
    else:
        BOT.send_message(message.chat.id, MSG_M_PASS_WRONG)
        session_request(message)


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
