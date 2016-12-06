# -*- coding: utf-8 -*-
#Author: Salil Shenoy
'''
The module is to get stock prices from the google finance. It will retrieve
historical stock price data.
'''

import pandas as pd
import urllib2
import datetime as dt


class RetrieveStockPrice(object):
    
    url = 'http://www.google.com/finance/getprices?i='
    
    def __init__(self, period, window):
        self.period = period        
        self.window = window
        self.url += str(self.period) + '&p=' + str(self.window)
        
    def getStockPrices(self, ticker):
        # The API will work for UPPER-CASE ticker values.
        ticker = ticker.upper()
        
        query = self.url + 'd&f=d,o,h,l,c&df=cpct&q=' + ticker
        response = urllib2.urlopen(query)
        data = response.read().split('\n')
        parsed_data = []
        anchor_stamp = ''
        end = len(data)
        for i in range(7, end):
            cdata = data[i].split(',')
            if 'a' in cdata[0]:
                anchor_stamp = cdata[0].replace('a', '')
                cts = int(anchor_stamp)
            else:
                try:
                    coffset = int(cdata[0])
                    cts = int(anchor_stamp) + (coffset * self.period) 
                    parsed_data.append((dt.datetime.fromtimestamp(float(cts)), \
                           float(cdata[1]), float(cdata[2]), float(cdata[3]), \
                           float(cdata[4])))
                except:
                    pass # for time zone offsets thrown into data
        df = pd.DataFrame(parsed_data)
        df.columns = ['ts', 'o', 'h', 'l', 'c']
        return df
        
    def getStockPricesForCompanies(self, tickers):
        
        stockPriceVsTicker = {}
        
        for ticker in tickers:
            df = self.getStockPrices(ticker)
            stockPriceVsTicker[ticker] = df
            
        return stockPriceVsTicker
