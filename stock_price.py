# -*- coding: utf-8 -*-
#Author: Salil Shenoy
'''
The module is to get stock prices from the National Stock Exchange. It uses the
nsetools library to get the quotes of stocks.
'''

from nsetools import Nse
from googlefinance import getQuotes
from yahoo_finance import Share
from pprint import pprint
import json

import pandas as pd
import numpy as np
import urllib2
import datetime as dt


class Stock_Price(object):
    
    def __init__(self):
        self.nse = Nse()
        self.url = 'http://www.google.com/finance/getprices?i='
        self.response = None
        self.data = None
        
    def get_price(self):
        #q = self.nse.get_quote('amzn')
        #pprint(q)
        #print json.dumps(getQuotes(['AMZN','VIE:BKS']), indent=2)
        q = Share('AMZN')
        pprint(q.get_historical('2016-12-02', '2016-12-03'))
        return
    
    def get_google_data(self, symbol, period, window):
        self.url += str(period) + '&p=' + str(window)
        self.url += 'd&f=d,o,h,l,c,v&df=cpct&q=' + symbol
        self.response = urllib2.urlopen(self.url)
        self.data = self.response.read().split('\n')
        parsed_data = []
        anchor_stamp = ''
        end = len(self.data)
        for i in range(7, end):
            cdata = self.data[i].split(',')
            if 'a' in cdata[0]:
            #first one record anchor timestamp
                anchor_stamp = cdata[0].replace('a', '')
                cts = int(anchor_stamp)
            else:
                try:
                    coffset = int(cdata[0])
                    cts = int(anchor_stamp) + (coffset * period)
                    parsed_data.append((dt.datetime.fromtimestamp(float(cts)), \
                           float(cdata[1]), float(cdata[2]), float(cdata[3]), \
                           float(cdata[4]), float(cdata[5])))
                except:
                    pass # for time zone offsets thrown into data
        df = pd.DataFrame(parsed_data)
        df.columns = ['ts', 'o', 'h', 'l', 'c', 'v']
        df.index = df.ts
        del df['ts']
        return df
    
def main():
    stock_price = Stock_Price()
    print stock_price.get_google_data('SPY', 300, 10)
    
if __name__ == '__main__':
    main()

