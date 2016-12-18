import json_parser as jpar
import RetrievePrice as rp
import constants as ct
import datetime as dt
import CreateDatabase as cdb
import os
from sklearn.linear_model import LinearRegression
from sklearn import cross_validation

reload(jpar)
reload(cdb)
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
import numpy as np
from scipy import stats

def linear_model_main(X_parameters,Y_parameters,predict_value):
 
    # Create linear regression object
    regr = linear_model.LinearRegression()
    regr.fit(X_parameters, Y_parameters)
    predict_outcome = regr.predict(predict_value)
    predictions = {}
    predictions['intercept'] = regr.intercept_
    predictions['coefficient'] = regr.coef_
    predictions['predicted_value'] = predict_outcome
    return predictions
    
def show_linear_line(X_parameters,Y_parameters):
    # Create linear regression object
    #print X_parameters,Y_parameters
    regr = linear_model.LinearRegression()
    regr.fit(X_parameters, Y_parameters)
    plt.scatter(X_parameters,Y_parameters,color='blue')
    plt.plot(X_parameters,regr.predict(X_parameters),color='red',linewidth=4)
    plt.xticks((X_parameters))
    plt.yticks([Y_parameters.min(), Y_parameters.max()])
    plt.show()
    
            
def main():
    createdb = cdb.CreateDatabase()
    parsedata = jpar.ParseData()
    
    #Apple, Samsung, Google, 
    companies = {'Apple':['iphone','macbook'], 'Samsung':['mobile'],'Microsoft':['windows']}
    company_articles  = {}          #Stores company and its corresponding article
    company_timestamp = {}         #Stores company and its corresponding timestamp

    # Get relevant data from json
    for company in companies:
        #print "Extracting articles from {0}".format(company)
        articles = parsedata.extractArticlesFromJSON(os.getcwd() + 
                   os.path.sep + ct._DATADICTIONARY + 
                   os.path.sep +'{0}.json'.format(company),company)
        company_articles[company] = articles
 
    for key in company_articles:
        temp = []
        articles = company_articles[key]
        for article in articles:
            #res = str(article.timestamp) + "_" + article.date[:8]
            res = article.timestamp
            temp.append(res)
            company_timestamp[key] = temp
            
    # Get Stock Price for past 30 days
    rs = rp.RetrieveStockPrice(300, 30)
    res = rs.getStockPricesForCompanies(['amzn','CSCO','IBM','INFY','SYMC','V'])
    df1 = res['amzn']
    #print df1


    news_articles = ['2016-11-08 04:21:00','2016-11-11 01:57:00', '2016-11-15 12:49:00', '2016-11-16 18:23:00', '2016-11-17 13:19:00', '2016-11-18 05:28:00', '2016-11-20 16:40:00', '2016-11-22 19:01:00', '2016-11-24 01:02:00', '2016-11-26 04:02:00', '2016-11-28 02:03:00', '2016-11-28 14:12:00', '2016-11-29 17:48:00', '2016-11-30 05:01:00', '2016-12-01 19:32:00', '2016-12-02 23:26:00', '2016-12-06 12:57:00', '2016-12-06 13:00:00']

    temp = ['2016-11-15 12:49:00']

    for i in temp:
        count=0
        temp = []
        for j in df1['ts']:
            if i <= str(j):
                break
            count += 1
        print df1.loc[count-3:count+3, 'ts']
        print df1.loc[count-3:count+3,:'o']
        x1 = df1.loc[count-3:count+3, 'ts']
        #x1 = df1.loc[count-6:count-1, 'ts']
        y1 = df1.loc[count-3:count+3, 'o']
        #x2 = df1.loc[count:count+5,:'']

        lr_x1_plot = [[-3],[-2],[-1],[0],[1],[2],[3]]
        lr_x1 = [-3,-2,-1,0,1,2,3]
        predict_value = 4
        #print "LENGHT", len(lr_x1), len(y1)
        

        slopeBArticle, interceptBArticle, r_valueBArticle, p_valueBArticle, std_errBArticle = stats.linregress(lr_x1[:4],y1[:4])
        print "\nStats from before the time the article was published : \n"
        print "\nSlope : %s\nIntercept : %s\n" % (slopeBArticle,interceptBArticle)
        
        slopeAArticle, interceptAArticle, r_valueAArticle, p_valueAArticle, std_errAArticle = stats.linregress(lr_x1[4:],y1[4:])
        print "\nStats from after the time the article was published : \n"
        print "\nSlope : %s\nIntercept : %s\n" % (slopeAArticle,interceptAArticle)
        
        print "The stock prices went %s after the publishing of the article.\n" % ('UP' if slopeAArticle - slopeBArticle > 0 else 'DOWN')
        
        show_linear_line(lr_x1_plot,y1)
        
        """
        result = linear_model_main(lr_x1,y1,predict_value)
        print "Intercept value " , result['intercept']
        print "coefficient" , result['coefficient']
        print "Predicted value: ",result['predicted_value']
        """
        
        
        """
        plt.plot(x1, y1)
        plt.suptitle(i)
        plt.xlabel("Time of Day")
        plt.ylabel("Stock Price (in USD)")
        plt.show()
        """


    '''for i in res:
        df = res[i]
        x = df.loc[1001:,'ts']
        #y = df.loc[:,'o':]
        y = df.loc[1001:, 'o']
        plt.plot(x,y)
        plt.suptitle(i)
        plt.xlabel("Time of Day")
        plt.ylabel("Stock Price (in USD)")
        plt.show()
    '''

    '''amazon_df  = res['amzn']
    x = list(range(0, 2324))
    x = np.reshape(x, (2324, 1))
    y = amazon_df.loc[:,'o']
    y = np.reshape(y, (2324, 1))
    reg = linear_model.LinearRegression()
    reg.fit(x,y)
    print

    regression = np.polyfit(x, y, 1)
    fit_fn = np.poly1d(regression)
    plt.plot(x, y, 'yo', x, fit_fn(x), '--k')
    plt.xlim(0.0, 1000.0)
    plt.ylim(0, 99999999999999999999)
'''
    #print "\nPrinting Stock prices : %s" % (res)
    relevant_sp = {}
    for org in company_timestamp.keys():
        for ts in company_timestamp[org]:
            relevant_sp[org] = {} 
    
    temp_ts = []
    
    for org in company_timestamp.keys():
        for ts in company_timestamp[org]:
            #ts_converted = dt.datetime.fromtimestamp(ts)
            #ts_converted_int = dt.datetime.utcfromtimestamp(1477315800) # Need this value
            #ts_converted = dt.datetime.utcfromtimestamp(1477315800).strftime('%m-%d-%Y %H:%M:%S')
            ts_converted = dt.datetime.utcfromtimestamp(ts)
            oneDayBeforeTS = (ts_converted + dt.timedelta(hours=-16)).strftime('%Y-%m-%d %H:%M:%S')
            oneDayAfterTS = (ts_converted + dt.timedelta(hours=16)).strftime('%Y-%m-%d %H:%M:%S')
            ts_converted = ts_converted.strftime('%Y-%m-%d %H:%M:%S')
            temp_ts.append(ts_converted)
            # Filter the stock prices for 16 hours before and after the news article
            #print "Time Stamp : %s\n1 Day Before : %s\n1 Day After : %s\n" % (ts,oneDayBeforeTS,oneDayAfterTS)
            relevant_sp[org] = res[ct._TICKERS[org]].loc[(res['CSCO']['ts'] >= oneDayBeforeTS) & (res['CSCO']['ts'] <= oneDayAfterTS)]
    #print "Relevant Stock Price : %s" % relevant_sp

if __name__ == "__main__":
    main()
