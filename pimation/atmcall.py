#!/usr/local/bin/python3

import matplotlib.pyplot as plt
import csv
from random import sample
from matplotlib import style
import datetime as dt
from mpl_finance import candlestick_ohlc
import pandas as pd
import pandas_datareader.data as web
import matplotlib.dates as mdates
from IPython.core.pylabtools import figsize

# d_dash = today.strftime("%Y-%m-%d")
watchlist = ['MSFT', 'V', 'DLR', 'CONE', 'PING', 'AMD', 'O', 'BAM', 'DDOG', 'ADBE', 'NKE', 'CHWY', 'NOK', 'BIP', 'O', 'DOCU', 'QCOM', 'BABA', 'DIS', 'ZS', 'NVDA', 'CCI', 'AMT', 'RTX']
# chart_dir = '/home/pi/Documents/automation/awtybot/'
# days = 365 # Stock data to chart against

def random_picks():
    figsize(14, 7)
    style.use('ggplot')
    stock_list = sample(watchlist, 4)
    print(f'random stock pick from watchlist ${stock_list}')
    chart_dir = '/Users/MisterFili/Documents/misc_files/'
    #set current date
    start = dt.datetime(2018, 1,1)
    end = dt.datetime(2020, 6,15)
    today = dt.datetime.now().date()
    end = dt.datetime(today.year, today.month,today.day)
    start = dt.datetime(today.year -1, today.month,today.day)
    
    for stock_pick in stock_list:
        # company_symbol = yf.Ticker(f'{stock_pick}')
        # data = company_symbol.history(period=f"{days}d")
        df = web.DataReader(f'{stock_pick}', 'yahoo', start=start, end=end)
        df.to_csv(f'{stock_pick}.csv')
        df = pd.read_csv(f'{stock_pick}.csv', parse_dates=True, index_col=0)
        #CHECK TO SEE IF MARKETS ARE OPEN
        

        df['200d_EMA'] = df.Close.ewm(span=200,min_periods=0,adjust=False,ignore_na=False).mean()
        df['50d_EMA'] = df.Close.ewm(span=50,min_periods=0,adjust=False,ignore_na=False).mean()     

        df_ohlc = df['Adj Close'].resample('10D').ohlc()
        df_volume = df['Volume'].resample('10D').sum()

        df_ohlc.reset_index(inplace=True)
        df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

        ax1 = plt.subplot2grid((6,1), (0,0), rowspan=4, colspan=1, title=f"${stock_pick} STOCK")
        ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1, label='Volume')
        # Plt.subplot2grid(shape, location, rowspan, colspan)

        candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
        ax1.plot(df.index, df[['200d_EMA']], label='200d_EMA')
        ax1.plot(df.index, df[['50d_EMA']], label='50d_EMA')
        ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0) #x and y 
        ax1.xaxis_date()
        ax1.legend()
        # fig= plt.figure(num=1, figsize=(6,3))
        plt.savefig(f'{chart_dir}{stock_pick}.png', bbox_inches='tight')
        print(chart_dir)
        # plt.show()
random_picks()