########################################################################################################################
# IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT ## IMPORT #
########################################################################################################################

# importing py files
from dir_telebot.tg_func import *


########################################################################################################################
# COMMANDS # COMMANDS # COMMANDS # COMMANDS # COMMANDS # COMMANDS # COMMANDS # COMMANDS # COMMANDS # COMMANDS # COMMANDS
########################################################################################################################

# setting commands
BOT.set_my_commands(
    [
        telebot.types.BotCommand("/help", "help"),
    ]
)


########################################################################################################################
# COMMAND HELP # COMMAND HELP # COMMAND HELP # COMMAND HELP # COMMAND HELP # COMMAND HELP # COMMAND HELP # COMMAND HELP
########################################################################################################################

# command: help
@BOT.message_handler(commands=['help'])
def startCoin(message):
    if check_user_id(message.from_user.id, message):
        instruction = MSG_I_MANUAL
        BOT.send_message(message.chat.id, instruction)


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
