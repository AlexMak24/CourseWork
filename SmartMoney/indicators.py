import pandas as pd
import pandas_ta as ta

def fvg(ohlc, join_consecutive=False):
    gaps = []
    for i in range(1, len(ohlc)-1):
        if ohlc['high'].iloc[i-1] < ohlc['low'].iloc[i+1]:
            gaps.append((1, ohlc['high'].iloc[i-1], ohlc['low'].iloc[i+1], None))
        elif ohlc['low'].iloc[i-1] > ohlc['high'].iloc[i+1]:
            gaps.append((-1, ohlc['high'].iloc[i+1], ohlc['low'].iloc[i-1], None))
        else:
            gaps.append((0, None, None, None))
    return pd.DataFrame(gaps, columns=['FVG', 'Top', 'Bottom', 'MitigatedIndex'], index=ohlc.index[1:-1])

def swing_highs_lows(ohlc, swing_length=50):
    ohlc['swing_high'] = ohlc['high'].rolling(window=swing_length).max()
    ohlc['swing_low'] = ohlc['low'].rolling(window=swing_length).min()
    return ohlc[['swing_high', 'swing_low']]

def liquidity(ohlc, swing_highs_lows, range_percent=0.01):
    liquidity_data = []
    for i in range(1, len(swing_highs_lows)):
        high_range = ohlc['high'].iloc[i] * range_percent
        low_range = ohlc['low'].iloc[i] * range_percent
        if ohlc['high'].iloc[i-1] < ohlc['high'].iloc[i] < ohlc['high'].iloc[i+1] and ohlc['high'].iloc[i] - ohlc['high'].iloc[i-1] < high_range:
            liquidity_data.append((1, ohlc['high'].iloc[i], i))
        elif ohlc['low'].iloc[i-1] > ohlc['low'].iloc[i] > ohlc['low'].iloc[i+1] and ohlc['low'].iloc[i-1] - ohlc['low'].iloc[i] < low_range:
            liquidity_data.append((-1, ohlc['low'].iloc[i], i))
        else:
            liquidity_data.append((0, None, None))
    return pd.DataFrame(liquidity_data, columns=['Liquidity', 'Level', 'Swept'], index=swing_highs_lows.index[1:])

def bos_choch(ohlc, swing_highs_lows, close_break=True):
    bos_choch_data = []
    for i in range(1, len(swing_highs_lows)):
        if swing_highs_lows['swing_high'].iloc[i-1] and ohlc['close'].iloc[i] > swing_highs_lows['swing_high'].iloc[i-1]:
            bos_choch_data.append((1, 1, ohlc['close'].iloc[i], i))
        elif swing_highs_lows['swing_low'].iloc[i-1] and ohlc['close'].iloc[i] < swing_highs_lows['swing_low'].iloc[i-1]:
            bos_choch_data.append((-1, -1, ohlc['close'].iloc[i], i))
        else:
            bos_choch_data.append((0, 0, None, None))
    return pd.DataFrame(bos_choch_data, columns=['BOS', 'CHOCH', 'Level', 'BrokenIndex'], index=swing_highs_lows.index[1:])

def ob(ohlc, swing_highs_lows, close_mitigation=False):
    ob_data = []
    for i in range(1, len(swing_highs_lows)):
        if swing_highs_lows['swing_high'].iloc[i-1]:
            top = ohlc['high'].iloc[i]
            bottom = ohlc['low'].iloc[i-1]
            volume = ohlc['volume'].iloc[i] + ohlc['volume'].iloc[i-1] + ohlc['volume'].iloc[i-2]
            percentage = min(ohlc['volume'].iloc[i-1], ohlc['volume'].iloc[i-2]) / max(ohlc['volume'].iloc[i-1], ohlc['volume'].iloc[i-2])
            ob_data.append((1, top, bottom, volume, percentage))
        elif swing_highs_lows['swing_low'].iloc[i-1]:
            top = ohlc['high'].iloc[i-1]
            bottom = ohlc['low'].iloc[i]
            volume = ohlc['volume'].iloc[i] + ohlc['volume'].iloc[i-1] + ohlc['volume'].iloc[i-2]
            percentage = min(ohlc['volume'].iloc[i-1], ohlc['volume'].iloc[i-2]) / max(ohlc['volume'].iloc[i-1], ohlc['volume'].iloc[i-2])
            ob_data.append((-1, top, bottom, volume, percentage))
        else:
            ob_data.append((0, None, None, None, None))
    return pd.DataFrame(ob_data, columns=['OB', 'Top', 'Bottom', 'OBVolume', 'Percentage'], index=swing_highs_lows.index[1:])

def previous_high_low(ohlc, time_frame="1D"):
    resampled = ohlc.resample(time_frame).agg({'high': 'max', 'low': 'min'})
    previous_high = resampled['high'].shift(1)
    previous_low = resampled['low'].shift(1)
    return previous_high, previous_low

def sessions(ohlc, session, start_time, end_time, time_zone="UTC"):
    ohlc.index = ohlc.index.tz_localize('UTC').tz_convert(time_zone)
    start_time = pd.to_datetime(start_time).time()
    end_time = pd.to_datetime(end_time).time()
    session_data = []
    for timestamp in ohlc.index:
        if start_time <= timestamp.time() <= end_time:
            session_data.append((1, ohlc.loc[timestamp]['high'], ohlc.loc[timestamp]['low']))
        else:
            session_data.append((0, None, None))
    return pd.DataFrame(session_data, columns=['Active', 'High', 'Low'], index=ohlc.index)

def retracements(ohlc, swing_highs_lows):
    retracement_data = []
    for i in range(1, len(swing_highs_lows)):
        if swing_highs_lows['swing_high'].iloc[i-1]:
            retracement = (ohlc['close'].iloc[i] - swing_highs_lows['swing_high'].iloc[i-1]) / (swing_highs_lows['swing_high'].iloc[i-1] - swing_highs_lows['swing_low'].iloc[i-1]) * 100
            retracement_data.append((1, retracement, retracement))
        elif swing_highs_lows['swing_low'].iloc[i-1]:
            retracement = (ohlc['close'].iloc[i] - swing_highs_lows['swing_low'].iloc[i-1]) / (swing_highs_lows['swing_high'].iloc[i-1] - swing_highs_lows['swing_low'].iloc[i-1]) * 100
            retracement_data.append((-1, retracement, retracement))
        else:
            retracement_data.append((0, None, None))
    return pd.DataFrame(retracement_data, columns=['Direction', 'CurrentRetracement%', 'DeepestRetracement%'], index=swing_highs_lows.index[1:])
