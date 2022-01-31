from os import error
import tweepy
import math
import yahoo_fin.stock_info as si
import pandas as pd
import yfinance as yf

class stock_class:
# data frame notes
# dataframe.iloc[row_section, col_section]
# dataframe.iloc[row_section]

    def __init__(self, stock_one, stock_two="None", stock_three="None", stock_four="None"):
        self.stock_one = stock_one
        self.stock_two = stock_two
        self.stock_three = stock_three
        self.stock_four = stock_four

    def income_statement(self):
        pass

    def cash_flow(self):
        pass

    def income_statement(self):
        pass
    
    def balance_sheet(self):
        bundle = [self.stock_one, self.stock_two, self.stock_three, self.stock_four]
        for symbol in bundle:
            try:
                sheet = si.get_balance_sheet(stock_class)
                stats = si.get_stats(symbol)
                sheet.cash
                sheet.longTermInvestments
                #balancesheet
                ebitda = stats[stats.Attribute == 'EBITDA']
                ebitda_value = ebitda['Value'].values[0]
                company = stock.upper()
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
            except Exception as e:
                print(e)
            tweet = f"DAILY STOCK\nStock: ${company}\nMarket Cap: ${market_cap}\n52 Week Range: ${fiftytwo_wk}\nClose: ${previous_close}\n1y Target Est: ${one_year_target}\nEPS (TTM): ${eps_ttm}\nPE Ratio (TTM) {pe_ratio}"
            
            # response = tweet_api.update_status(status=tweet)
            # original_tweet = original_tweet.id
            # tweet_id = response.id
            ### to respond to a tweet ####
            # status=textforreply, 
            #         in_reply_to_status_id=original_twee.id
            #          auto_populate_reply_metadata=True#

            print(f'tweet sent!\n{tweet}')
            print(f'tweet Char Count: {len(tweet)}')
        return tweet

    def percent_conversion(self, value):
        try:
            percent = value * 100
            p = '{0:.4g}'.format(percent)
            return p
        except Exception as e:
            print(e)

    def get_mkt_cap(self, n):
        millnames = ['',' Thousand','M','B','T']
        n = float(n)
        millidx = max(0,min(len(millnames)-1,
                            int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
        return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

    def technicals(self):
        bundle = [self.stock_one, self.stock_two, self.stock_three, self.stock_four]
        for symbol in bundle:
            try:
                company = yf.Ticker(f'{symbol}')
                print(f'pulling technicals for {symbol}:\n')
                sector = company.info['sector']
                symbol = company.info['symbol']
                current_price = company.info["currentPrice"]
                #
                a_vol = company.info["averageDailyVolume10Day"]
                avg_vol = "{:,}".format(a_vol)
                v = company.info["volume"]
                vol = "{:,}".format(v)
                #
                fDA = company.info["fiftyDayAverage"]
                fiftyDayAverage = round(fDA, 2)
                tDA = company.info["twoHundredDayAverage"]
                twoHundredDayAverage = round(tDA, 2)
                #
                fiftyTwoWeekLow = company.info["fiftyTwoWeekLow"]
                fiftyTwoWeekHigh = company.info["fiftyTwoWeekHigh"]
                recs = company.recommendations
                latest = recs.iloc[-1]
                firm = latest.iloc[0]
                grade = latest.iloc[1]
                action = latest.iloc[3]
                if action == "main":
                    action = "Maintains"
                elif action == "down":
                    action = "Downgraded"
                elif action == "up":
                    action = "Upgraded"
                elif action == "init":
                    action = "Initiated"
                tweet = f"${symbol}\nPrice: ${current_price}\n52wkLow: ${fiftyTwoWeekLow}\n52wkHigh: ${fiftyTwoWeekHigh}\n50dma(orng): ${fiftyDayAverage}\n200dma(grn): ${twoHundredDayAverage}\nVol: {vol}\navg10dVol: {avg_vol}"
                # Rec: {firm} grades {symbol} with a {grade} - {action}
                print(len(tweet))
                print(tweet)
                return tweet
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
            except Exception as e:
                print(e)

    def basic_fundamentals(self):
        bundle = [self.stock_one, self.stock_two, self.stock_three, self.stock_four]
        for symbol in bundle:
            try:
                company = yf.Ticker(f'{symbol}')
                print(f'pulling fundamentals for {symbol}:\n')
                sector = company.info['sector']
                symbol = company.info['symbol']
                priceToSalesTrailing12Months = company.info["priceToSalesTrailing12Months"]
                if priceToSalesTrailing12Months is None:
                    priceToSalesTrailing12Months = "n/a"
                    print(f'priceToSalesTrailing12Months set to 0 for {symbol}')
                ps = round(company.info["priceToSalesTrailing12Months"], 2)
                #
                t_eps = company.info["trailingEps"]
                trailingEPS = self.percent_conversion(t_eps)
                roa = company.info["returnOnAssets"]
                roa_percent = self.percent_conversion(roa)
                roe = company.info["returnOnEquity"]
                roe_percent = self.percent_conversion(roe)
                gp = company.info["grossProfits"]
                gross_profits = self.get_mkt_cap(gp)
                ##
                mk = float(company.info['marketCap'])
                marketCap = self.get_mkt_cap(mk)
                ##
                profit_margins = company.info["profitMargins"]
                profit_margins_percent = self.percent_conversion(profit_margins)
                gross_margins = company.info["grossMargins"]
                gross_margins_percent = self.percent_conversion(gross_margins)
                ##


                # earningsGrowth
                # revenuePerShare
                # forwardEps
                # revenueQuarterlyGrowth
                # bookValue
                # trailingEps
                # threeYearAverageReturn
                # earningsQuarterlyGrowth
                # ytdReturn
                # fiveYearAverageReturn
                # trailingPE
                ### BALANCE SHEET ###
                #####################
                # PE
                # ebitda
                # priceToBook
                # pegRatio
                # totalCash
                # totalCashPerShare
                # totalDebt
                # debtToEquity
                # currentRatio
                # bookValue
                # Book Value Per Share (mrq)
                # #
                # heldPercentInstitutions
                
                # market_cap = get_mkt_cap(marketCap)
                # return market_cap
                tweet = f"${symbol}\nP/S(ttm): {ps}\nROE: {roe_percent}%\nROA: {roa_percent}%\nGross Profit: {gross_profits}\nGross Margin: {gross_margins_percent}%\nProfit Margins: {profit_margins_percent}%\nEPS(ttm): ${trailingEPS}"
                print(len(tweet))
                print(tweet)
                return tweet
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
            except Exception as e:
                print(e)
