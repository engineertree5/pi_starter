#!/usr/local/bin/python3

import yfinance as yf
import matplotlib.pyplot as plt
from random import sample
import csv
from datetime import date
###
import tweepy
from secrets import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# constructing API instance
api = tweepy.API(auth)
user = api.get_user('lordfili')


# GLOBAL VARS
today = date.today()
d_slash = today.strftime("%Y/%m/%d")
d_dash = today.strftime("%Y-%m-%d")
watchlist = ['MSFT', 'V', 'DLR', 'CONE', 'PING', 'AMD', 'O', 'BAM', 'DDOG', 'ADBE', 'NKE', 'CHWY', 'NOK', 'BIP', 'O', 'DOCU', 'QCOM', 'BABA', 'DIS', 'ZS', 'NVDA', 'CCI', 'AMT', 'RTX']
chart_dir = '/home/pi/Documents/automation/awtybot/'
days = 365 # Stock data to chart against


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
        

        data['50d_EMA'] = data.Close.ewm(span=50,min_periods=0,adjust=False,ignore_na=False).mean()
        data['20d_EMA'] = data.Close.ewm(span=20,min_periods=0,adjust=False,ignore_na=False).mean()
        data['100d_EMA'] = data.Close.ewm(span=100,min_periods=0,adjust=False,ignore_na=False).mean()
        

        fig, ax = plt.subplots()
        data[['Close', '50d_EMA', '100d_EMA', '20d_EMA']].plot(title=f"${stock_pick} STOCK {d_dash}", figsize=(10,5), ax=ax)
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
    stock_list = random_picks()
    update_status(stock_list)

if __name__ == "__main__":
    main()
