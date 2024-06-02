########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# lib
import re
import requests
import logging as logger
from threading import Thread

# dir: head
from dir_pumpBot.pb_head import *

# dir: func
from dir_telebot.tg_commands import *


########################################################################################################################
# MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN # MAIN #
########################################################################################################################

# function: main
def main():
    while True:
        try:

            # message
            print('Telegram bot is starting')
            print()

            # bot running
            BOT.polling(none_stop=True)

        # exception
        except Exception as E:
            user = usr.get_user()

            # sending Exception in dir_telebot
            BOT.send_message(user.user_id, "ERROR: " + str(E))

            # setting logger config
            logger.basicConfig(
                filename='__system__/errors/errors.txt',
                filemode='a',
                format='%(asctime)s, %(message)s',
                datefmt='%d/%m/%Y_%T'
            )

            # logging Exception
            logger.error(E)

            # sending last dir_user safe-shot
            file_user_txt = open('dir_user/storage/user_current.txt', 'rb')
            BOT.send_document(user.user_id, file_user_txt)


########################################################################################################################
# __NAME__ # __NAME__ # __NAME__ # __NAME__ # __NAME__ # __NAME__ # __NAME__ # __NAME__ # __NAME__ # __NAME__ # __NAME__
########################################################################################################################

# __name__ check
if __name__ == '__main__':

    # calling main function
    main()


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
