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
watchlist = ['NOK', 'NOK']
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
        #  If True -> try parsing the index. dates are stored @ column 0

        #CHECK TO SEE IF MARKETS ARE OPEN
        invert_df = df.sort_index(axis=0, ascending=False)
        mkt_date_check = invert_df.loc[d_dash]
        # if mkt_date_check.empty == True:
        #     print('dataframe empty!\n!!MARKET CLOSED!!')
        #     print('exiting')
        #     exit(1)
        #     # raise RuntimeError('data is empty')
        # else:
        #     print('MARKET OPEN!')
        # Resampling the time series data based on months 
        # we apply it on stock close price 
        # 'M' indicates month 
        # monthly_resampled_data = df.close.resample('M').mean() 
        df['200d_EMA'] = df.Close.ewm(span=200,min_periods=0,adjust=False,ignore_na=False).mean()
        df['26d_EMA'] = df.Close.ewm(span=26,min_periods=0,adjust=False,ignore_na=False).mean()     
        df['12d_EMA'] = df.Close.ewm(span=12,min_periods=0,adjust=False,ignore_na=False).mean()   

        #calculate the MCAD
        df['mcad'] = df['12d_EMA'] - df['26d_EMA']

        df['macdsignal'] = df['mcad'].ewm(span=9, adjust=False).mean()

        df_ohlc = df['Adj Close'].resample('W-Fri').ohlc()
        # df_ohlc = df['Adj Close'].resample('5D').ohlc() THIS WAS A MISTAKE ######
        # new dataframe, based on df['Adj Close']column, resamped with a 10 day window

        df_volume = df['Volume'].resample('W-Fri').sum() #This will give you ohlc data for the week ending on a Friday.
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
        ax1.plot(df.index, df[['26d_EMA']], label='26d_EMA')
        ax1.plot(df.index, df[['12d_EMA']], label='12d_EMA')
        # ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0) #x and y 
        ax1.xaxis_date() # converts the axis from the raw mdate numbers to dates.
        ax1.legend()
        ax2.legend()

        plt.savefig(f'{chart_dir}{stock_pick}{edition}.png', bbox_inches='tight')
random_picks()