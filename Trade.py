import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


data = yf.download('NVDA', start='2022-05-12', end='2024-07-02')

short_window = 40
long_window = 100

data['Short_MA'] = data['Close'].rolling(window=short_window, min_periods=1).mean()
data['Long_MA'] = data['Close'].rolling(window=long_window, min_periods=1).mean()

data['Signal'] = 0
data['Signal'][short_window:] = np.where(data['Short_MA'][short_window:] > data['Long_MA'][short_window:], 1, 0)
data['Position'] = data['Signal'].diff()

plt.figure(figsize=(10,5))
plt.plot(data['Close'], label='Close Price', color='g')
plt.plot(data['Short_MA'], label=f'Short {short_window} MA', color='r', linestyle='--')
plt.plot(data['Long_MA'], label=f'Long {long_window} MA', color='b', linestyle='--')

plt.plot(data[data['Position'] == 1].index, 
         data['Short_MA'][data['Position'] == 1], 
         '^', markersize=10, color='m', label='Buy Signal')

plt.plot(data[data['Position'] == -1].index, 
         data['Short_MA'][data['Position'] == -1], 
         'v', markersize=10, color='k', label='Sell Signal')

plt.title('Stock Price and Moving Averages')
plt.legend()
plt.show()
