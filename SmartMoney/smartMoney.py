import pandas as pd
import matplotlib.pyplot as plt
from indicators import fvg, swing_highs_lows, liquidity, bos_choch, ob, previous_high_low, retracements
import numpy as np

# Загрузка данных из CSV файла
data = pd.read_csv('1day.csv')
# Удаление последнего столбца
data = data.iloc[:, :-1]

def previous_high_low_custom(ohlc, time_frame="1D"):
    ohlc.index = pd.to_datetime(ohlc.index)

    previous_high = np.zeros(len(ohlc), dtype=np.float32)
    previous_low = np.zeros(len(ohlc), dtype=np.float32)

    resampled_ohlc = ohlc.resample(time_frame).agg(
        {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        }
    ).dropna()

    for i in range(len(ohlc)):
        resampled_previous_index = np.where(resampled_ohlc.index < ohlc.index[i])[0]
        if len(resampled_previous_index) <= 1:
            previous_high[i] = np.nan
            previous_low[i] = np.nan
            continue
        resampled_previous_index = resampled_previous_index[-2]

        previous_high[i] = resampled_ohlc["high"].iloc[resampled_previous_index]
        previous_low[i] = resampled_ohlc["low"].iloc[resampled_previous_index]

    return previous_high, previous_low


# Убедитесь, что столбцы имеют правильные имена и формат
data.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp', inplace=True)
data_without_timestamp = data[['open', 'high', 'low', 'close', 'volume']].copy()
print(data_without_timestamp)
from smartmoneyconcepts import smc

# Применение всех индикаторов
# Применение индикаторов
fvg_data = smc.fvg(data_without_timestamp, join_consecutive=False)
swing_highs_lows_data = smc.swing_highs_lows(data_without_timestamp, swing_length=50)
bos_choch_data = smc.bos_choch(data_without_timestamp, swing_highs_lows_data, close_break=True)
order_blocks_data = smc.ob(data_without_timestamp, swing_highs_lows_data, close_mitigation=False)
liquidity_data = smc.liquidity(data_without_timestamp, swing_highs_lows_data, range_percent=0.01)
previous_high, previous_low = previous_high_low_custom(data_without_timestamp, time_frame="1D")
retracements_data = smc.retracements(data_without_timestamp, swing_highs_lows_data)


# Создание DataFrame из массивов NumPy
previous_high_df = pd.DataFrame(previous_high, index=data_without_timestamp.index, columns=["PreviousHigh"])
previous_low_df = pd.DataFrame(previous_low, index=data_without_timestamp.index, columns=["PreviousLow"])

# Сохранение в файлы CSV
previous_high_df.to_csv('previous_high.csv')
previous_low_df.to_csv('previous_low.csv')
# Сохранение результатов каждого индикатора в отдельный файл
fvg_data.to_csv('fvg_data.csv')
swing_highs_lows_data.to_csv('swing_highs_lows_data.csv')
bos_choch_data.to_csv('bos_choch_data.csv')
order_blocks_data.to_csv('order_blocks_data.csv')
liquidity_data.to_csv('liquidity_data.csv')
retracements_data.to_csv('retracements_data.csv')

# Объединение всех сигналов в один DataFrame
indicators = pd.concat(
    [fvg_data, swing_highs_lows_data, bos_choch_data, order_blocks_data, liquidity_data, previous_high_df, previous_low_df, retracements_data], axis=1)

# Преобразуйте индекс в тип DatetimeIndex
indicators.index = pd.to_datetime(indicators.index)

print(indicators)

# Установка начального баланса и параметров торговли
initial_balance = 10000
tp = 0.05  # Take Profit 5%
sl = 0.02  # Stop Loss 2%
trade_size = initial_balance / 10  # Условная величина каждой сделки

# Создаем список для хранения P&L каждой сделки
pnl_list = []

def trading_strategy(data, indicators, entry_threshold, exit_threshold):
    signals = []
    balance = initial_balance
    count = 1
    in_position = False  # Флаг, указывающий, находимся ли мы в позиции
    # Проходим по данным, применяя торговую стратегию
    for i in range(len(data)):
        if indicators['FVG'][i] > entry_threshold and not in_position:
            # Вход в позицию
            count = count+1
            entry_price = data['close'][i]
            tp_price = entry_price * (1 + tp)
            sl_price = entry_price * (1 - sl)
            signals.append((data.index[i], 'buy', entry_price, tp_price, sl_price))
            in_position = True

        elif indicators['FVG'][i] < -exit_threshold and in_position:
            # Выход из позиции
            exit_price = data['close'][i]
            pnl = trade_size * (exit_price - entry_price)
            pnl_list.append(pnl)
            balance += pnl
            in_position = False
            if pnl < 0:
                print(f"Проигрышная сделка: Время входа:{count} ', Цена входа: {entry_price}, "
                      f"Цена выхода: {exit_price}, Прибыль/убыток: {pnl}",f"balance: {balance}")
            in_position = False

    return pnl_list, balance

# Выполнение торговой стратегии
pnl_list, final_balance = trading_strategy(data, indicators, entry_threshold=0.7, exit_threshold=0.3)

print(f"Initial Balance: ${initial_balance:.2f}, Final Balance: ${final_balance:.2f}")


entry_threshold = 0.7
exit_threshold = 0.3
# Визуализация графика торговой пары с маркировкой входа и выхода из позиции
plt.figure(figsize=(14, 7))
plt.plot(data.index, data['close'], label='Close Price', color='blue')
for i in range(1, len(data)):
    if indicators['FVG'][i] > entry_threshold:
        plt.scatter(data.index[i], data['close'][i], color='green', marker='^', label='Buy Signal')
    elif indicators['FVG'][i] < exit_threshold:
        plt.scatter(data.index[i], data['close'][i], color='red', marker='v', label='Sell Signal')
plt.title('Trading Signals on Close Price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()