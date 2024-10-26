import pandas as pd

def calculate_rsi(prices, window=14):
    """
    Calculate the Relative Strength Index (RSI) for a series of prices.
    
    :param prices: List of historical closing prices
    :param window: The window period for the RSI (typically 14)
    :return: The RSI value
    """
    prices_series = pd.Series(prices)
    delta = prices_series.diff(1)
    
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = round(100 - (100 / (1 + rs)),4)
    
    return rsi.iloc[-1]  # Return the last RSI value


def calculate_ema_50(prices, window=50):
    """
    Calculate the Exponential Moving Average (EMA) for a series of prices.
    
    :param prices: List of historical closing prices
    :param window: The window period for the EMA (e.g., 50 for 50-day EMA)
    :return: The EMA value
    """
    prices_series = pd.Series(prices)
    ema = round(prices_series.ewm(span=window, adjust=False).mean(),5)
    return ema.iloc[-1]  # Return the last EMA value

def calculate_ema_200(prices, window=200):
    """
    Calculate the Exponential Moving Average (EMA) for a series of prices.
    
    :param prices: List of historical closing prices
    :param window: The window period for the EMA (e.g., 50 for 50-day EMA)
    :return: The EMA value
    """
    prices_series = pd.Series(prices)
    ema = round(prices_series.ewm(span=window, adjust=False).mean(),5)
    return ema.iloc[-1]  # Return the last EMA value


def get_trade_signal(rsi, ema_50, ema_200, current_price):
    if ema_50 > ema_200 and rsi < 40 and current_price > ema_200:
        return "Strong Buy"
    elif ema_50 > ema_200 and rsi < 50 and current_price > ema_200:
        return "Moderate Buy"
    elif ema_50 < ema_200 and rsi > 60 and current_price < ema_200:
        return "Strong Sell"
    elif ema_50 < ema_200 and rsi > 50 and current_price < ema_200:
        return "Moderate Sell"
    else:
        return "Hold"




# def get_trade_signal(rsi, ema_50, ema_200, current_price):
#     # Sell signal if 50-day EMA is below 200-day EMA OR current price is less than either 50-day or 200-day EMA
#     if ema_50 < ema_200 and rsi > 60 and current_price < ema_200:
#         return "Sell"
    
#     # Buy signal if 50-day EMA is above 200-day EMA AND current price is above both EMAs
#     elif ema_50 > ema_200 and rsi < 40 and current_price > ema_200:
#         return "Buy"
    
#     # Default to Hold signal if no other conditions are met
#     else:
#         return "Hold"
    


# def get_trade_signal(rsi, ema, current_price):
#     if rsi < 30 and current_price > ema:
#         return "Buy"
#     elif rsi > 70 and current_price < ema:
#         return "Sell"
#     else:
#         return "Hold"
