import yfinance as yf
import pandas as pd

def fetch_stock_data(stock):
    try:
        data = yf.download(stock, period="3mo")
        data = data.tail(60).reset_index()
        data.columns = [col.lower() for col in data.columns]
        return data.to_dict(orient='list')
    except Exception as e:
        return {"close": [0]*60}

def sma(df, period):
    return sum(df['close'][-period:]) / period

def calculate_rsi(df, period=14):
    import numpy as np
    close = df['close']
    delta = [close[i] - close[i - 1] for i in range(1, len(close))]
    gain = [x if x > 0 else 0 for x in delta]
    loss = [-x if x < 0 else 0 for x in delta]
    avg_gain = sum(gain[-period:]) / period
    avg_loss = sum(loss[-period:]) / period
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    return 100 - (100 / (1 + rs))
