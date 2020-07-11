#!/usr/local/bin/python3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import mpl_finance as mpf 

# watchlist = ['MSFT', 'V', 'DLR', 'CONE', 'PING', 'AMD', 'O', 'BEP', 'DDOG', 'ADBE', 'NKE', 'CHWY', 'NOK', 'BIP', 'O', 'DOCU', 'QCOM', 'BABA', 'DIS', 'ZS', 'NVDA', 'CCI', 'AMT', 'RTX', 'BYND', 'RDFN', 'PI', 'ROKU', 'TDOC', 'ERIC', 'TCEHY', 'PINS']
chart_dir = '/Users/MisterFili/Documents/misc_files/jupyterholder/'
today = dt.datetime.now().date()
end = dt.datetime(today.year, today.month,today.day)
start = dt.datetime(today.year -1, today.month,today.day)
d_dash = today.strftime("%Y-%m-%d")

stock_pick = 'ERIC'
# df = web.DataReader(f'{stock_pick}', 'yahoo', start=start, end=end)
# df.to_csv(f'{stock_pick}.csv')
df = pd.read_csv(f'{stock_pick}.csv', parse_dates=True, index_col=0) #  If True -> try parsing the index. dates are stored @ column 0

df.index = pd.to_datetime(df.index)

# We need to exctract the OHLC prices into a list of lists:
dvalues = df[['Open', 'High', 'Low', 'Close']].values.tolist()

# Dates in our index column are in datetime format, we need to comvert them 
# to Matplotlib date format (see https://matplotlib.org/3.1.1/api/dates_api.html):
pdates = mdates.date2num(df.index)

# We prepare a list of lists where each single list is a [date, open, high, low, close] sequence:
ohlc = [ [pdates[i]] + dvalues[i] for i in range(len(pdates)) ]

fig, ax = plt.subplots(figsize = (12,6))

mpf.candlestick_ohlc(ax, ohlc[-35:], width=0.4)
ax.set_xlabel('Date')
ax.set_ylabel('Price ($)')
ax.set_title(f'{stock_pick} - Candlestick Chart')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))

fig.autofmt_xdate()

plt.show()