########################################################################################################################
# IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # IMPORT # I
########################################################################################################################

# importing libraries
import time
import json
import requests
import websocket
from datetime import datetime

# importing directories: func
from dir_math import mth_func as mth
from dir_user import user_func as usr
from dir_front import front_func as frnt


########################################################################################################################
# SOCKET # SOCKET # SOCKET # SOCKET # SOCKET # SOCKET # SOCKET # SOCKET # SOCKET # SOCKET # SOCKET # SOCKET # SOCKET # S
########################################################################################################################

# class: Socket
class Socket:

    # constructor
    def __init__(self, url, symbol):

        # CHECK
        self.i = 0

        self.list_time = []
        self.list_price = []

        self.list_percents = dict()
        self.list_SMAs = dict()
        self.list_SDs = dict()

        self.list_c_vol_BUY = []
        self.list_c_vol_SELL = []

        self.list_SD_c_vol_BUY = []
        self.list_SD_c_vol_SELL = []

        # declaring class fields: main
        self.symbol = symbol.upper()
        self.status_bool, self.status_time, self.status_price = True, 0, 0

        # declaring class fields: check points
        self.cp_1_bool, self.cp_1_time, self.cp_1_price = False, 0, 0
        self.cp_2_bool, self.cp_2_time, self.cp_2_price = False, 0, 0

        # declaring class fields: websocket
        self.url = url
        self.ws = websocket.WebSocketApp(
            url,
            on_open=self.on_open,
            on_close=self.on_close,
            on_message=self.on_message,
            on_error=self.on_error
        )

        # declaring class fields: common values
        self.price = 0
        # self.Ns = [8, 4, 2]
        # self.Ns = [128, 64, 32, 8, 2]
        self.Ns = [128, 64, 32, 16, 8, 4, 2]
        # self.Ns = [1024, 512, 256, 128, 64, 32, 16, 8, 4, 2]

        # CHECK
        for n in self.Ns:
            self.list_percents['percent_' + str(n)] = []
            self.list_SMAs['SMA_' + str(n)] = []
            self.list_SDs['SD_' + str(n)] = []

        # declaring class fields: past volume
        self.vol = 0
        self.vol_BUY = 0
        self.vol_SELL = 0

        # declaring class fields: percents
        self.percents = dict()
        self.SMAs = dict()
        self.SDs = dict()

        # declaring class fields: current volume
        self.c_vol = 0
        self.c_vol_BUY = 0
        self.c_vol_SELL = 0

        # declaring class fields: SMA
        self.SMA_c_vol_BUY = 0
        self.SMA_c_vol_SELL = 0

        # declaring class fields: SD
        self.SD_c_vol_BUY = 0
        self.SD_c_vol_SELL = 0

        # declaring class fields: data (main data)
        self.data = dict()
        self.data_keys = [
            'time',
            'price',
            'vol', 'c_vol',
            'vol_BUY', 'c_vol_BUY',
            'vol_SELL', 'c_vol_SELL',
            'SMA_c_vol_BUY', 'SMA_c_vol_SELL',
            'SD_c_vol_BUY', 'SD_c_vol_SELL'
        ]
        for n in self.Ns:
            self.data_keys.append('percent_' + str(n))
            self.data_keys.append('SMA_' + str(n))
            self.data_keys.append('SD_' + str(n))
        for i in self.data_keys:
            self.data[i] = []
            [self.data[i].append(None) for _ in range(self.Ns[0])]

        # running websocket forever
        self.ws.run_forever()

    ####################################################################################################################
    # ON MESSAGE # ON MESSAGE # ON MESSAGE # ON MESSAGE # ON MESSAGE # ON MESSAGE # ON MESSAGE # ON MESSAGE # ON MESSAGE
    ####################################################################################################################

    # callback function: websocket send message
    def on_message(self, ws, message):
        data_msg = json.loads(message)

        # saving common values (from message)
        self.price = float(data_msg['k']['c'])

        # calculating current values: volumes, trades
        c_vol = float(data_msg['k']['v']) - self.vol
        c_vol_BUY = float(data_msg['k']['V']) - self.vol_BUY
        c_vol_SELL = (float(data_msg['k']['v']) - float(data_msg['k']['V'])) - self.vol_SELL

        # saving current values (from message)
        self.c_vol = c_vol if (c_vol > 0) else self.c_vol
        self.c_vol_BUY = c_vol_BUY if (c_vol_BUY > 0) else self.c_vol_BUY
        self.c_vol_SELL = c_vol_SELL if (c_vol_SELL > 0) else self.c_vol_SELL

        # saving past values (from message)
        self.vol = float(data_msg['k']['v'])
        self.vol_BUY = float(data_msg['k']['V'])
        self.vol_SELL = self.vol - self.vol_BUY

        # calculating extra values
        if self.data['price'][-1] is not None:
            for n in self.Ns:
                N = self.Ns[0]
                p = 'percent_' + str(n)

                self.percents[p] = self.data['price'][0] / self.data['price'][:n][-1] - 1
                self.SMAs['SMA_' + str(n)] = mth.calculate_SMA(self.data[p])
                self.SDs['SD_' + str(n)], _ = mth.calculate_SDs_fast(self.data[p], self.SMAs['SMA_' + str(n)], N, 4)

                self.SMA_c_vol_BUY = mth.calculate_SMA(self.data['c_vol_BUY'])
                self.SMA_c_vol_SELL = mth.calculate_SMA(self.data['c_vol_SELL'])

                self.SD_c_vol_BUY, _ = mth.calculate_SDs_fast(self.data['c_vol_BUY'], self.SMA_c_vol_BUY, N, 4)
                self.SD_c_vol_SELL, _ = mth.calculate_SDs_fast(self.data['c_vol_SELL'], self.SMA_c_vol_SELL, N, 4)
        else:
            for n in self.Ns:
                self.percents['percent_' + str(n)] = 0
                self.SMAs['SMA_' + str(n)] = 0
                self.SDs['SD_' + str(n)] = 0

                self.SMA_c_vol_BUY = 0
                self.SMA_c_vol_SELL = 0

                self.SD_c_vol_BUY = 0
                self.SD_c_vol_SELL = 0

        # saving values (in data)
        new_list = [
            int(time.time()),
            self.price,
            self.vol, self.c_vol,
            self.vol_BUY, self.c_vol_BUY,
            self.vol_SELL, self.c_vol_SELL,
            self.SMA_c_vol_BUY, self.SMA_c_vol_SELL,
            self.SD_c_vol_BUY, self.SD_c_vol_SELL
        ]
        for n in self.Ns:
            new_list.append(self.percents['percent_' + str(n)])
            new_list.append(self.SMAs['SMA_' + str(n)])
            new_list.append(self.SDs['SD_' + str(n)])
        for i in range(len(new_list)):
            self.data[self.data_keys[i]].insert(0, new_list[i])
            self.data[self.data_keys[i]].pop()

        # CHECK
        self.list_time.append(self.data['time'][0])
        self.list_price.append(self.data['price'][0])
        for n in self.Ns:
            self.list_percents['percent_' + str(n)].append(self.data['percent_' + str(n)][0])
            self.list_SMAs['SMA_' + str(n)].append(self.data['SMA_' + str(n)][0])
            self.list_SDs['SD_' + str(n)].append(self.data['SD_' + str(n)][0])
        self.list_c_vol_BUY.append(self.data['c_vol_BUY'][0])
        self.list_c_vol_SELL.append(self.data['c_vol_SELL'][0])
        self.list_SD_c_vol_BUY.append(self.SD_c_vol_BUY)
        self.list_SD_c_vol_SELL.append(self.SD_c_vol_SELL)

        # CHECK
        print(self.i, self.data)

        # CHECK
        if self.i != self.Ns[0] + 5:
            self.i += 1
        else:
            x = [datetime.fromtimestamp(timestamp) for timestamp in self.list_time]
            y = [
                [
                    {'name': 'price', 'data': self.list_price, 'log': False},
                ],
                [
                    {'name': 'c_BUY', 'data': self.list_c_vol_BUY, 'log': False},
                    {'name': '+4sd', 'data': self.list_SD_c_vol_BUY, 'log': False},
                    {'name': 'c_SELL', 'data': self.list_c_vol_SELL, 'log': False},
                    {'name': '+4sd', 'data': self.list_SD_c_vol_SELL, 'log': False},
                ],
            ]
            for n in self.Ns:
                d = [
                    {'name': 'percent_' + str(n), 'data': self.list_percents['percent_' + str(n)], 'log': False},
                    {'name': 'SMA', 'data': self.list_SMAs['SMA_' + str(n)], 'log': False},
                    {'name': '+4sd', 'data': self.list_SDs['SD_' + str(n)], 'log': False},
                ]
                y.append(d)
            plot = frnt.get_shared_plot(self.symbol.upper(), x, y)
            plot.show()

        ################################################################################################################
        # ALGORITHM # ALGORITHM # ALGORITHM # ALGORITHM # ALGORITHM # ALGORITHM # ALGORITHM # ALGORITHM # ALGORITHM # AL
        ################################################################################################################

        # data is ready to start algorithm
        if self.data['price'][-1] is not None:
            if self.status_bool:
                user = usr.get_user()
                chat_id = user.chat_id
                token = user.token
                url = f'https://api.telegram.org/bot{token}/sendMessage'

                # check point: check
                if not self.cp_1_bool:
                    for n in self.Ns:
                        key_p = 'percent_' + str(n)
                        key_s = 'SD_' + str(n)

                        check_1 = self.percents[key_p] > self.SDs[key_s]
                        check_2 = self.c_vol_BUY > self.SD_c_vol_BUY

                        # check point: passed
                        if check_1 and check_2:
                            self.cp_1_bool = True
                            self.cp_1_time = self.data['time'][0]
                            self.cp_1_price = self.data['price'][0]

                            # message
                            message = f'Date: {datetime.fromtimestamp(self.cp_1_time).date()}' + '\n' \
                                      f'Time: {datetime.fromtimestamp(self.cp_1_time).time()}' + '\n' \
                                      f'\n' \
                                      f'- - - - - - - - - - - -' + '\n' \
                                      f'Side: SHORT' + '\n' \
                                      f'Power: {n}' + '\n' \
                                      f'Symbol: {str(self.symbol)}' + '\n' \
                                      f'Price: {self.cp_1_price}' + '\n' \
                                      f'- - - - - - - - - - - -' + '\n' \

                            requests.post(url, json={'chat_id': chat_id, 'text': message})
                            print(message)

                            self.cp_1_bool, self.cp_1_time, self.cp_1_price = False, 0, 0

                        # breaking on first signal
                        break

    ####################################################################################################################
    # ON OPEN # ON OPEN # ON OPEN # ON OPEN # ON OPEN # ON OPEN # ON OPEN # ON OPEN # ON OPEN # ON OPEN # ON OPEN # ON O
    ####################################################################################################################

    # callback function: websocket opened
    def on_open(self, ws):
        print(f'Websocket: opened [{self.symbol}]')

    ####################################################################################################################
    # ON CLOSE # ON CLOSE # ON CLOSE # ON CLOSE # ON CLOSE # ON CLOSE # ON CLOSE # ON CLOSE # ON CLOSE # ON CLOSE # ON C
    ####################################################################################################################

    # callback function: websocket closed
    def on_close(self, ws, close_status_code, close_msg):
        print(f'Websocket: closed [{self.symbol} | {close_status_code} | {close_msg}]')

    ####################################################################################################################
    # ON ERROR # ON ERROR # ON ERROR # ON ERROR # ON ERROR # ON ERROR # ON ERROR # ON ERROR # ON ERROR # ON ERROR # ON E
    ####################################################################################################################

    # callback function: websocket errored
    def on_error(self, ws, error):
        print(f'Websocket: error [{self.symbol} | {error}]')


########################################################################################################################
# END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END # END
########################################################################################################################
