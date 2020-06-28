#!/usr/local/bin/python3

import yfinance as yf
import matplotlib.pyplot as plt
from random import sample
import csv
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import pandas as pd
import pandas_datareader.data as web
import matplotlib.dates as mdates
from IPython.core.pylabtools import figsize
###
import tweepy
from secrets import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# constructing API instance
api = tweepy.API(auth)
user = api.get_user('lordfili')


# GLOBAL VARS
watchlist = ['MSFT', 'V', 'DLR', 'CONE', 'PING', 'AMD', 'O', 'BAM', 'DDOG', 'ADBE', 'NKE', 'CHWY', 'NOK', 'BIP', 'O', 'DOCU', 'QCOM', 'BABA', 'DIS', 'ZS', 'NVDA', 'CCI', 'AMT', 'RTX']
chart_dir = '/home/pi/Documents/automation/awtybot/'
days = 365 # Stock data to chart against

def candle_picks():
    figsize(14, 7)
    style.use('ggplot')
    stock_list = sample(watchlist, 4)
    print(f'random stock pick from watchlist ${stock_list}')
    #set current date
    today = dt.datetime.now().date()
    end = dt.datetime(today.year, today.month,today.day)
    start = dt.datetime(today.year -1, today.month,today.day)
    pick_info = {}
    pick_info['symbols'] = {}
    for stock_pick in stock_list:
        company_symbol = yf.Ticker(f'{stock_pick}')
        data = company_symbol.history(period=f"{days}d")
        try:
            s_name = company_symbol.get_info()['shortName']
        except IndexError as err:
            s_name = '*'
            print(err)
        pick_info['symbols'][stock_pick] = s_name
        
        df = web.DataReader(f'{stock_pick}', 'yahoo', start=start, end=end)
        df.to_csv(f'{stock_pick}.csv')
        df = pd.read_csv(f'{stock_pick}.csv', parse_dates=True, index_col=0)
        

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
        # plt.show()
    return pick_info

def random_picks():
    stock_list = sample(watchlist, 4)
    print(f'random stock pick from watchlist ${stock_list}')
    pick_info = {}
    pick_info['symbols'] = {}
    for stock_pick in stock_list:
        company_symbol = yf.Ticker(f'{stock_pick}')
        data = company_symbol.history(period=f"{days}d")
        try:
            s_name = company_symbol.get_info()['shortName']
        except IndexError as err:
            s_name = '*'
            print(err)
        pick_info['symbols'][stock_pick] = s_name

        #CHECK TO SEE IF MARKETS ARE OPEN
        invert_company_ema = company_symbol.history(period=f"{days}d").sort_index(axis=0, ascending=False)
        mkt_date_check = invert_company_ema.loc[d_dash]
        # if mkt_date_check.empty == True:
        #     print('dataframe empty!\n!!MARKET CLOSED!!')
        #     print('exiting')
        #     exit(0)
        #     # raise RuntimeError('data is empty')
        # else:
        #     print('MARKET OPEN!') 
        # shortname = company_symbol.get_info()['shortName']
        

        data['50d_SMA'] = data.Close.rolling(window=50).mean()
        data['100d_SMA'] = data.Close.rolling(window=100).mean()
        data['200d_SMA'] = data.Close.rolling(window=200).mean()

        fig, ax = plt.subplots()
        data[['Close', '50d_SMA', '100d_SMA', '200d_SMA']].plot(title=f"${stock_pick} STOCK {d_dash}", figsize=(10,5), ax=ax)
        # Don't allow the axis to be on top of your data
        ax.set_axisbelow(True)
        ax.grid()

        plt.savefig(f'{chart_dir}{stock_pick}.png')
    print(pick_info)  
    return pick_info
    
def update_status(pick_info):
    # using tweepy API to update status
    try:
        statement = []
        stock_list = []
        for stock, shortname in pick_info['symbols'].items():
            statement.append(stock + " - " + shortname)
            stock_list.append(stock)

        feels = f'${statement[0]}\n${statement[1]}\n${statement[2]}\n${statement[3]}\n'
        print(feels)
        print(f"{chart_dir}{stock_list[3]}.png")
        media0 = api.media_upload(f"{chart_dir}{stock_list[0]}.png")
        media1 = api.media_upload(f"{chart_dir}{stock_list[1]}.png")
        media2 = api.media_upload(f"{chart_dir}{stock_list[2]}.png")
        media3 = api.media_upload(f"{chart_dir}{stock_list[3]}.png")
        api.update_status(status=feels, media_ids=[media0.media_id,media1.media_id,media2.media_id,media3.media_id])
        print('tweet sent!\n',feels)
    
    except tweepy.TweepError as e:
        print(e.reason)
        print(e.api_code)
        print(e.response.text)

def main():
    stock_list = candle_picks()
    update_status(stock_list)

if __name__ == "__main__":
    main()
