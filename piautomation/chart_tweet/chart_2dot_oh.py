import yfinance as yf
from random import sample
import csv
import datetime as dt
import matplotlib
import pandas as pd
import fundamentals
import pandas_datareader.data as web
import mplfinance as mpf

import tweepy
from secrets import *

yf.pdr_override()

#### FOR RUNNING HEADLESS MODE ### export MPLBACKEND=Agg
matplotlib.use('Agg') # will need to create env var for running headless. 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

# constructing twitter API instance
api = tweepy.API(auth)
user = api.get_user('lordfili')

### Setting date values
today = dt.datetime.now().date()
start = dt.datetime(today.year -1, today.month, today.day) # current day
start = start.strftime('%Y-%m-%d').lstrip("0").replace(" 0", " ")
end = dt.datetime(today.year, today.month,today.day) # X days ago
d_dash = today.strftime("%Y-%m-%d")

#### Stock Watchlist, data directory, days of chart
chart_dir = '/home/pi/Documents/automation/awtybot/'
days = 365 # Stock data to chart against
# Sort alpabeticaly -- $:sorted(stocklist)
stocklist = ['AMD', 'APPS', 'AMRS', 'AXON', 'BOMN', 'BLFS', 'BIOX', 'CDXS', 'CAT', 'CLPT', 'CRWD', 'DDOG', 'DOCU', 'ETSY','EGLX', 'FLGT', 'HYPR', 'GLBE', 'GXO', 'INMD', 'JOE', 'JYNT', 'KOPN', 'KKR', 'KRYS', 'LMND', 'RICK', 'MELI', 'MGNI', 'MQ', 'NET', 'NARI', 'NNOX', 'NIO', 'NVDA', 'NNI', 'NTDOY', 'NVCR', 'OM', 'ORMP', 'PINS', 'PLTR', 'PSNL', 'PUBM', 'ROKU', 'SE', 'SOFI', 'SKLZ', 'SLNH', 'SMH', 'SHOP', 'SMLR', 'SDGR', 'SQ', 'SWAV', 'TDOC', 'TMDX', 'TTD', 'WIMI', 'WST', 'VERI', 'U', 'UPST', 'XPEV', 'XPEL']

sample_selection = sample(stocklist, 4)

def get_stock_fundamentals(stock):
    try:
        company = yf.Ticker(f'{stock}')
        shortName = company.info['shortName']
        symbol = company.info['symbol']
    except IndexError as err:
        shortName = '*'
        print(err)
        print(f'NO INFO: {stock}')

    return symbol, shortName


def stock_pick(symbol, company_name):
    
    #### Pass in stock ticker, download stock data as csv, create chart, save chart ####
    #### DEFINE KWARGS
    kwargs = dict(type='candle',mav=(20,50,200),volume=True,figratio=(11,8),figscale=0.9, title=f'{company_name} ${symbol}') 
    df = web.get_data_yahoo(f'{symbol}',start=start, end=end)
    # df = web.DataReader(f'{symbol}', 'yahoo', start=start, end=end)
    df.to_csv(f'{symbol}.csv')
    df = pd.read_csv(f'{symbol}.csv', parse_dates=True, index_col=0)
    # mpf.plot(df,**kwargs,style='yahoo',tight_layout=True,savefig=dict(fname='tsave100.png',dpi=500))
    axes = mpf.plot(df,style='yahoo', **kwargs,fill_between=0.03,datetime_format="%b-%Y", xrotation=0,
    scale_width_adjustment=dict(volume=0.4, candle=1.50), tight_layout=True, ylabel='', ylabel_lower='', savefig=dict(fname=f'{chart_dir}{symbol}.png',dpi=500))

def update_status(pick_info):
    # using tweepy API to update status
    count = 0
    print(pick_info)
    try:
        statement = []
        stock_list = []
        for stock, shortname in pick_info['symbols'].items():
            statement.append(stock + " - " + shortname)
            stock_list.append(stock)

            print(statement[count])
            print("********")
            print(stock)
            print("********")
            #Get Technical Info
            techies = fundamentals.stock_class(stock)
            stock_techies = techies.technicals()
            full_tweet = f"{stock_techies}"
            media = api.media_upload(f"{chart_dir}{stock_list[count]}.png")
            first_tweet_id = api.update_status(status=full_tweet, media_ids=[media.media_id])
            ## Chain Fundamental Tweet
            ftID = first_tweet_id.id
            fundy = fundamentals.stock_class(stock)
            stock_fundy = fundy.basic_fundamentals()
            fundy_tweet = f"{stock_fundy}"
            api.update_status(status=fundy_tweet, in_reply_to_status_id=ftID, auto_populate_reply_metadata=True)
            #replay to response ID with more fundamental info
            print(f'tweet sent! {full_tweet}\n{fundy_tweet}')
            print(len(full_tweet))
            count +=1

    
    except tweepy.TweepError as e:
        print(e.reason)
        print(e.api_code)
        print(e.response.text)

#MA line color 200d=gr, 50=ylw, 20=blu

def main():

    symbol_list = []
    pick_info = {}
    pick_info['symbols'] = {}

    for stock in sample_selection:
        values = get_stock_fundamentals(stock)
        # stock_pick(*values)
        symbol_list.append(values)
    #convert tuple list to dict
    
    dict_of_picks = dict(symbol_list)
    print(dict_of_picks)
    pick_info['symbols'] = dict_of_picks
    
    for i in dict.items(pick_info['symbols']):
        stock_pick(*i)

        #send out that work
    update_status(pick_info)

if __name__ == "__main__":
    main()