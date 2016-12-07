import json_parser as jpar
import RetrievePrice as rp
import constants as ct
import datetime as dt
import CreateDatabase as cdb
import os

reload(jpar)
reload(cdb)

def main():
    createdb = cdb.CreateDatabase()
    parsedata = jpar.ParseData()
    
    #Apple, Samsung, Google, 
    companies = {'Apple':['iphone','macbook'], 'Samsung':['mobile'],'Microsoft':['windows']}
    company_articles  = {}          #Stores company and its corresponding article
    company_timestamp = {}         #Stores company and its corresponding timestamp
    
    for company, entities in companies.items():
        try:
            company_articles[company] = createdb.GetArchivesNYT(company, entities) 
        except:
            print 'No information about ', company
            
    for company in company_articles.keys():
        print company 
        for value in company_articles[company]:
            createdb.news_org_api(value['url'])
            
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
            
    # Get Stock Price for past 60 days
    rs = rp.RetrieveStockPrice(300, 60)
    res = rs.getStockPricesForCompanies(['amzn','CSCO','IBM','INFY','SYMC','V'])
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
            relevant_sp[org][ts_converted] = res[ct._TICKERS[org]].loc[(res[ct._TICKERS[org]]['ts'] >= oneDayBeforeTS) & (res[ct._TICKERS[org]]['ts'] <= oneDayAfterTS)]
    print "Relevant Stock Price : %s" % relevant_sp
    print "No of distinct timestamps : ", relevant_sp[org].keys()#, len(company_timestamp[org]), company_timestamp[org], temp_ts

if __name__ == "__main__":
    main()
