# -*- coding: utf-8 -*-
#Author: Salil Shenoy
'''
The module is to get stock prices from the google finance. It will retrieve
historical stock price data.
'''

# Currently not using any of the following libraries.
#from nsetools import Nse
#from googlefinance import getQuotes
#from yahoo_finance import Share
from pprint import pprint
import pandas as pd
import urllib2
import datetime as dt


class RetrieveStockPrice(object):
    
    def __init__(self):
        #self.nse = Nse()
        self.url = 'http://www.google.com/finance/getprices?i='
        self.response = None
        self.data = None
        
    # Not used
    def get_price(self):
        q = Share('AMZN')
        pprint(q.get_historical('2016-12-02', '2016-12-03'))
        return
    
    def get_google_data(self, symbol, period, window):
        self.url += str(period) + '&p=' + str(window)
        self.url += 'd&f=d,o,h,l,c&df=cpct&q=' + symbol
        self.response = urllib2.urlopen(self.url)
        self.data = self.response.read().split('\n')
        parsed_data = []
        anchor_stamp = ''
        end = len(self.data)
        for i in range(7, end):
            cdata = self.data[i].split(',')
            if 'a' in cdata[0]:
                anchor_stamp = cdata[0].replace('a', '')
                cts = int(anchor_stamp)
            else:
                try:
                    coffset = int(cdata[0])
                    cts = int(anchor_stamp) + (coffset * period)
                    parsed_data.append((dt.datetime.fromtimestamp(float(cts)), \
                           float(cdata[1]), float(cdata[2]), float(cdata[3]), \
                           float(cdata[4])))
                except:
                    pass # for time zone offsets thrown into data
        df = pd.DataFrame(parsed_data)
        df.columns = ['ts', 'o', 'h', 'l', 'c']
        df.index = df.ts
        del df['ts']
        return df
