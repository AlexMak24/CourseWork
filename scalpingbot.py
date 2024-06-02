import pandas as pd
# Load the dataset from a CSV file
df=pd.read_csv("BTCUSD_Candlestick_15_M_ASK_05.08.2019-29.04.2022.csv")

# Clean 'Gmt time' column
df["Gmt time"]=df["Gmt time"].str.replace(".000","")
df['Gmt time']=pd.to_datetime(df['Gmt time'],format='%d.%m.%Y %H:%M:%S')
df.set_index("Gmt time", inplace=True)
df=df[df.High!=df.Low]
# Calculate Volume Weighted Average Price (VWAP) and Exponential Moving Average (EMA)
import pandas_ta as ta

# Calculate EMASignal
# Iterate over the DataFrame to determine bullish (2), bearish (1), or neutral (0) signals based on EMA
# Store the signals in the 'EMASignal' column

df["VWAP"]=ta.vwap(df.High, df.Low, df.Close, df.Volume)

# Calculate VWAPSignal
# Iterate over the DataFrame to determine bullish (2), bearish (1), or neutral (0) signals based on VWAP
# Store the signals in the 'VWAPSignal' column

df["EMA"]=ta.ema(df.Close, length=100)

emasignal = [0]*len(df)
backcandles = 6

for row in range(backcandles, len(df)):
    upt = 1
    dnt = 1
    for i in range(row-backcandles, row+1):
        if df.High[i]>=df.EMA[i]:
            dnt=0
        if df.Low[i]<=df.EMA[i]:
            upt=0
    if upt==1 and dnt==1:
        #print("!!!!! check trend loop !!!!")
        emasignal[row]=3
    elif upt==1:
        emasignal[row]=2
    elif dnt==1:
        emasignal[row]=1

df['EMASignal'] = emasignal


VWAPsignal = [0]*len(df)
backcandles = 3

for row in range(backcandles, len(df)):
    upt = 1
    dnt = 1
    for i in range(row-backcandles, row+1):
        if df.High[i]>=df.VWAP[i]:
            dnt=0
        if df.Low[i]<=df.VWAP[i]:
            upt=0
    if upt==1 and dnt==1:
        #print("!!!!! check trend loop !!!!")
        VWAPsignal[row]=3
    elif upt==1:
        VWAPsignal[row]=2
    elif dnt==1:
        VWAPsignal[row]=1

df['VWAPSignal'] = VWAPsignal

# Calculate TotalSignal
# Determine total signal based on EMASignal, VWAPSignal, and other conditions
# Store the signals in the 'TotalSignal' column

def TotalSignal(l):
    myclosedistance = 100
    if (df.EMASignal[l] == 2 and df.VWAPSignal[l] == 2  # and df.EngulfingSignal[l]==2
            and min(abs(df.VWAP[l] - df.High[l]), abs(df.VWAP[l] - df.Low[l])) <= myclosedistance):
        return 2
    if (df.EMASignal[l] == 1 and df.VWAPSignal[l] == 1  # and df.EngulfingSignal[l]==1
            and min(abs(df.VWAP[l] - df.High[l]), abs(df.VWAP[l] - df.Low[l])) <= myclosedistance):
        return 1


TotSignal = [0] * len(df)
for row in range(0, len(df)):  # careful backcandles used previous cell
    TotSignal[row] = TotalSignal(row)
df['TotalSignal'] = TotSignal

import numpy as np

# Calculate the price position break for TotalSignal
# If TotalSignal is bullish (2), set pointposbreak slightly above the high price
# If TotalSignal is bearish (1), set pointposbreak slightly below the low price
# Otherwise, set it as NaN
def pointposbreak(x):
    if x['TotalSignal']==1:
        return x['High']+1e-3
    elif x['TotalSignal']==2:
        return x['Low']-1e-3
    else:
        return np.nan

df['pointposbreak'] = df.apply(lambda row: pointposbreak(row), axis=1)

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# Plot candlestick chart with EMA and VWAP
# Add markers for TotalSignal

dfpl = df[1500:1900]
dfpl.reset_index(inplace=True)
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['Open'],
                high=dfpl['High'],
                low=dfpl['Low'],
                close=dfpl['Close']),
                go.Scatter(x=dfpl.index, y=dfpl.EMA, line=dict(color='orange', width=1), name="EMA"),
                go.Scatter(x=dfpl.index, y=dfpl.VWAP, line=dict(color='blue', width=1), name="VWAP")])

fig.add_scatter(x=dfpl.index, y=dfpl['pointposbreak'], mode="markers",
                marker=dict(size=5, color="MediumPurple"),
                name="Signal")
fig.show()

dfpl = df[:].copy()
dfpl.reset_index(inplace=True)
import pandas_ta as ta
dfpl['ATR']=ta.atr(dfpl.High, dfpl.Low, dfpl.Close, length=5)
#help(ta.atr)
def SIGNAL():
    return dfpl.TotalSignal


# Define the trading strategy class
# Initialize initial size, signal, and other parameters
# Define initialization and trading logic
# Implement buy and sell actions based on signals and ATR

from backtesting import Strategy
from backtesting import Backtest


class MyStrat(Strategy):
    initsize = 0.99
    mysize = initsize

    def init(self):
        super().init()
        self.signal1 = self.I(SIGNAL)

    def next(self):
        super().next()
        slatr = 0.8 * self.data.ATR[-1]
        TPSLRatio = 2

        if self.signal1 == 2 and len(self.trades) == 0:
            sl1 = self.data.Close[-1] - slatr
            tp1 = self.data.Close[-1] + slatr * TPSLRatio
            self.buy(sl=sl1, tp=tp1, size=self.mysize)

        elif self.signal1 == 1 and len(self.trades) == 0:
            sl1 = self.data.Close[-1] + slatr
            tp1 = self.data.Close[-1] - slatr * TPSLRatio
            self.sell(sl=sl1, tp=tp1, size=self.mysize)

# Run backtesting with the defined strategy
# Print statistics and plot results

bt = Backtest(dfpl, MyStrat, cash=100000, margin=1 / 5, commission=.00)
stat = bt.run()
print(stat)
bt.plot()