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
watchlist = ['MSFT', 'V', 'DLR', 'CONE', 'PING', 'AMD', 'O', 'BAM', 'DDOG', 'ADBE', 'NKE', 'CHWY', 'NOK', 'BIP', 'O', 'DOCU', 'QCOM', 'BABA', 'JNJ', 'DIS', 'T', 'NVDA', 'CCI', 'AMT', 'RTX']
chart_dir = '/home/pi/Documents/automation/awtybot/'
days = 365 # Stock data to chart against



def random_picks():
    stock_list = sample(watchlist, 4)
    print(f'random stock pick from watchlist ${stock_list}')
    for stock_pick in stock_list:
        company_symbol = yf.Ticker(f'{stock_pick}')
        company_history = company_symbol.history(period=f"{days}d")

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
        data = company_history

        data['50d_SMA'] = data.Close.rolling(window=50).mean()
        data['100d_SMA'] = data.Close.rolling(window=100).mean()
        data['200d_SMA'] = data.Close.rolling(window=200).mean()

        fig, ax = plt.subplots()
        data[['Close', '50d_SMA', '100d_SMA', '200d_SMA']].plot(title=f"${stock_pick} STOCK {d_dash}", figsize=(10,5), ax=ax)
        # Don't allow the axis to be on top of your data
        ax.set_axisbelow(True)
        ax.grid()

        plt.savefig(f'{chart_dir}{stock_pick}.png')
    return stock_list
def update_status(stock_list):
    
    
    # using tweepy API to update status
    try:
        statement = []
        for stock in stock_list:
            # stock_name = stock.info['shortName']
            statement.append(f'${stock}')
        feels = f'{statement[0]}\n{statement[1]}\n{statement[2]}\n{statement[3]}\n'
        media0 = api.media_upload(f"{chart_dir}{stock_list[0]}.png")
        media1 = api.media_upload(f"{chart_dir}{stock_list[1]}.png")
        media2 = api.media_upload(f"{chart_dir}{stock_list[2]}.png")
        media3 = api.media_upload(f"{chart_dir}{stock_list[3]}.png")
        api.update_status(status=feels, media_ids=[media0.media_id,media1.media_id,media2.media_id,media3.media_id])
        # api.update_status(status=feels)
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
