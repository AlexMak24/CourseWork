########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# lib
from threading import Thread

# dir: head
from dir_pumpBot.pb_head import Socket


########################################################################################################################
# START THREADS # START THREADS # START THREADS # START THREADS # START THREADS # START THREADS # START THREADS # START
########################################################################################################################

# function: main
def start_threads():
    symbols = ['tomousdt']
    # symbols = ['btcdomusdt']

    # starting websocket thread
    for symbol in symbols:
        url_ws = f'wss://fstream.binance.com/ws/{symbol}@kline_1m'
        Thread(target=Socket, args=(url_ws, symbol,)).start()


########################################################################################################################
# START THREADS # START THREADS # START THREADS # START THREADS # START THREADS # START THREADS # START THREADS # START
########################################################################################################################
