#! /usr/local/Cellar/python/3.7.4/bin/python3
import pandas as pd
import csv
import os
import yfinance as yf
import numpy as np
import subprocess
import math
import gspread
from os import system
import json
import requests
###
import tweepy
from secrets import *
# This script will be used to follow, update, and show my investing progress throughout the year(s) to come. 
### HOW DOES IT WORK ###
# Pull in .csv file which has stock picks
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
token = token
# constructing API instance
api = tweepy.API(auth)
user = api.get_user('lordfili')

def get_mkt_cap(n):
    millnames = ['',' Thousand','M','B','T']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

def get_close(stock):
    try:
        df = stock.history(period=f"5d")
        close_price = df['Close'].iloc[-1]    
    except IndexError as err:
        s_name = '*'
        print(err)
    return close_price

def get_all_stocks():
    pass

def get_portfolio(portfolio):
    gc = gspread.service_account()
    sh = gc.open(portfolio)
    df = pd.DataFrame(sh.sheet1.get_all_records())
    symbol_set = df['Symbol'] #assigning Symbol column to var
    # df['sector'] = np.nan #creating column called 'sector' and storing 'NaN' as place holder value. 
    df['PS_TTM'] = np.nan
    # df = df['gains'] = df['Quantity'] - df['total_gain%']
    for symbol in symbol_set:
        try:
            company = yf.Ticker(f'{symbol}')
            # sector = company.info['sector']
            symbol = company.info['symbol']
            priceToSalesTrailing12Months = company.info["priceToSalesTrailing12Months"]
            if priceToSalesTrailing12Months is None:
                priceToSalesTrailing12Months = 0
            shortName = company.get_info()['shortName']
            fiftyTwoWeekLow = company.info["fiftyTwoWeekLow"]
            fiftyTwoWeekHigh = company.info["fiftyTwoWeekHigh"]
            fiftyDayAverage = company.info["fiftyDayAverage"]
            twoHundredDayAverage = company.info["twoHundredDayAverage"]
            
            marketCap = float(company.info['marketCap'])
            market_cap = get_mkt_cap(marketCap)

            PS_TTM = round(priceToSalesTrailing12Months, 2)
            _50d_ma = round(fiftyDayAverage, 2)
            _200d_ma = round(twoHundredDayAverage, 2)
            # previousClose = company.info['previousClose']
            market_close = get_close(company)
            #### Assignments take place
            # df.loc[df['Symbol'] == f'{symbol}', 'sector'] = f'{sector}' # not necessary right now
            df.loc[df['Symbol'] == f'{symbol}', 'PS_TTM'] = f'{PS_TTM}'
            # df.loc[df['Symbol'] == f'{symbol}', '200d_ma'] = f'{_200d_ma}' # not necessary right now
            df.loc[df['Symbol'] == f'{symbol}', '50d_ma'] = f'{_50d_ma}'
            df.loc[df['Symbol'] == f'{symbol}', '200d_ma'] = f'{_200d_ma}'
            df.loc[df['Symbol'] == f'{symbol}', 'market_close'] = f'{market_close}'
            df.loc[df['Symbol'] == f'{symbol}', 'market_cap'] = f'{market_cap}'

        except KeyError as err:
            sector = 'N/A'
            symbol = company.info['symbol']
            print(f'{symbol} sector not found {sector}')
        except TypeError as err:
            print(f'{symbol} showing {err}')
            PS_TTM = 'Nan'
            print('setting Nan for PS_TTM')
            pass
        except IndexError as err:
            print(f'{symbol} showing {err}')
    try:
        df['market_close'] = pd.to_numeric(df['market_close']) #convert to numeric value
        df['purchase_price'] = pd.to_numeric(df['purchase_price']) #convert to numeric value
        df['50d_ma'] = pd.to_numeric(df['50d_ma']) #convert to numeric value
        df['200d_ma'] = pd.to_numeric(df['200d_ma']) #convert to numeric value
        df['total_gain%'] = pd.to_numeric(df['total_gain%']) #convert to numeric value
        df['total_gain%'] = ((df['market_close'] - df['purchase_price']) / df['purchase_price'] * 100 ).round(2)
        df['above_50dma'] = np.where((df['market_close'] > df['50d_ma']), True, False)
        df['above_200dma'] = np.where((df['market_close'] > df['200d_ma']), True, False)
                
    except KeyError as err:
        print(f'error {KeyError}')
    pd.set_option('mode.chained_assignment', None) # https://www.dataquest.io/blog/settingwithcopywarning/
    df.sort_values('Symbol')
    answer = int(df['total_gain%'].sum(skipna=True))
    total_count = df['PS_TTM'].count()
    total_percent = answer / total_count
    df['overall_%_gain'] ='' # creating a column called overall_%_gain
    df['overall_%_gain'][0] = round(total_percent, 2) # w/ use of '({do_math_here})' we insert answer var into the 0 index of column
    
    df.to_csv(f'/home/pi/Desktop/{portfolio}.csv', index=False) #save results to file

def del_csv():
    list_url = 'https://api.github.com/users/engineertree5/gists'
    headers = {'Authorization': f'token {token}'}
    r = requests.get(list_url, headers=headers)
    cleanup = (r.json())

    for gist in cleanup:
        files = gist['files']
        gist_id = gist['id']
        try:
            if files['all_positions.csv']['filename'] == 'all_positions.csv':
                print(f'{gist_id} to be deleted')
                print('deleteing gist')
                del_url = f'https://api.github.com/gists/{gist_id}'
                print(del_url)
                r = requests.delete(del_url, headers=headers)
                # print(r.json())
            else:
                print('notworking')
        except KeyError as e:
            print(f'{e}')

def push_csv():
    try:  
        df = pd.read_csv('/home/pi/Desktop/all_positions.csv')
        query_url = "https://api.github.com/gists"
        sample = df.to_csv(index=False)
        headers = {'Authorization': f'token {token}'}
        r = requests.post(query_url, headers=headers, data=json.dumps({"public":True,'files':{"all_positions.csv":{"content":sample}}}))
        print('gist updated')
        pct_change = df['overall_%_gain'][0]
        total_count = df['PS_TTM'].count()
        
        losers = get_losers()
        tweet_status = f"YTD Change: {pct_change}%\n# of positions: {total_count}\n{losers}\nView performance here (all_positions.csv): https://gist.github.com/engineertree5"
        print(tweet_status)
        api.update_status(status=tweet_status)
    except IndexError as e:
        print(e)

def get_losers():
    # Each column in a DataFrame is a Series. As a single column is selected, the returned object is a pandas Series.

    df = pd.read_csv('/home/pi/Desktop/all_positions.csv')
    df = df.sort_values(by = 'total_gain%')
    losers = df[['Symbol', 'total_gain%']][0:3]
    losers.reset_index(inplace=True)
    # Stor df into list
    symbol_list = []
    gain_percent = []
    for symbol in losers['Symbol']:
        symbol_list.append('$' + symbol)

    for percent in losers['total_gain%']:
        gain_percent.append(percent)        

    #convert to int to strings
    new_list = [str(x) for x in gain_percent]
    percent_list = []
    for gain in new_list:
        percent_list.append(gain + "%")

    #combining 2 list into 1 dict
    toploser = {}
    for symbol in symbol_list:
        for percent in percent_list:
            toploser[symbol] = percent
            percent_list.remove(percent)
            break
    
    pretty_list = []
    for loser in toploser:
        pretty_list.append((loser,toploser[loser]))
    
    x = pretty_list[0] 
    y = pretty_list[1] 
    z = pretty_list[2]

    a = ' '.join(x)
    b = ' '.join(y)
    c = ' '.join(z)

    return f"Top Losers:\n{a}\n{b}\n{c}"

all_holdings = 'all_positions'
get_portfolio(all_holdings) #insert which porfolio you would want to use
del_csv()
push_csv()
# get_losers()