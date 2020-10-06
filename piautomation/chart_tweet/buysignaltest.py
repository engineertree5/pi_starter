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

# watchlist = ['MSFT', 'V', 'DLR', 'CONE', 'PING', 'AMD', 'O', 'BEP', 'DDOG', 'ADBE', 'NKE', 'CHWY', 'NOK', 'BIP', 'O', 'DOCU', 'QCOM', 'BABA', 'DIS', 'ZS', 'NVDA', 'CCI', 'AMT', 'RTX', 'BYND', 'RDFN', 'PI', 'ROKU', 'TDOC', 'ERIC', 'TCEHY', 'PINS']
watchlist = ['AMD', 'AMD']
def random_picks():
    figsize(14, 7) # creates an inch-by-inch image
    style.use('ggplot') # ggplot is a data visualization pkg
    stock_list = sample(watchlist, 1) # pick a random 4 stocks 
    print(f'random stock pick from watchlist ${stock_list}')
    chart_dir = '/Users/MisterFili/Documents/misc_files/'
    #set current date & 1 year from now
    today = dt.datetime.now().date()
    end = dt.datetime(today.year, today.month,today.day)
    start = dt.datetime(today.year -1, today.month,today.day)
    d_dash = today.strftime("%Y-%m-%d")
    
    for stock_pick in stock_list:
        # df = web.DataReader(f'{stock_pick}', 'yahoo', start=start, end=end)
        # df.to_csv(f'{stock_pick}.csv')
        df = pd.read_csv(f'{stock_pick}.csv', parse_dates=True, index_col=0)

        df['bullishSignal'] = (df.Low < df.Low.shift(1).rolling(13).min()) & (df.Close > ((df.High - df.Low) / 2 + df.Low))
        markers_on = df['bullishSignal']
        df['200d_EMA'] = df.Close.ewm(span=200,min_periods=0,adjust=False,ignore_na=False).mean()
        df['50d_EMA'] = df.Close.ewm(span=50,min_periods=0,adjust=False,ignore_na=False).mean()     
        df['20d_EMA'] = df.Close.ewm(span=20,min_periods=0,adjust=False,ignore_na=False).mean()     
        
        #calculations for MACD
        df['26d_EMA'] = df.Close.ewm(span=26,min_periods=0,adjust=False,ignore_na=False).mean()     
        df['12d_EMA'] = df.Close.ewm(span=12,min_periods=0,adjust=False,ignore_na=False).mean()   
        
        #calculate the MCAD
        df['mcad'] = df['12d_EMA'] - df['26d_EMA']
        df['macdsignal'] = df['mcad'].ewm(span=9, adjust=False).mean()

        df_ohlc = df['Adj Close'].resample('W-Fri').ohlc()
        # df_volume = df['Volume'].resample('W-Fri').sum() #This will give you ohlc data for the week ending on a Friday.
        
        edition = 87
        df_ohlc.reset_index(inplace=True)
        # don't want date to be an index anymore, reset_index
        # dates is just a regular column. Next, we convert it
        df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

        ax1 = plt.subplot2grid((6,1), (0,0), rowspan=4, colspan=1, title=f"${stock_pick} STOCK")
        ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1, title="MACD")

        candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g', alpha=0.7)

        ax2.plot(df.index, df[['macdsignal']], label='Signal')
        ax2.plot(df.index, df[['mcad']], label='MCAD')
        ax1.plot(df.index, df[['20d_EMA']], label='20d_EMA')
        ax1.plot(df.index, df[['50d_EMA']], label='50d_EMA')
        ax1.plot(df.index, df[['200d_EMA']], label='200d_EMA')
        ax1.plot(df.index, dfmarkevery=markers_on, label='bullsignal')
        # ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0) #x and y 
        ax1.xaxis_date() # converts the axis from the raw mdate numbers to dates.
        ax1.legend()
        ax2.legend()
        plt.show()
        # plt.savefig(f'{chart_dir}{stock_pick}{edition}.png', bbox_inches='tight')
random_picks()