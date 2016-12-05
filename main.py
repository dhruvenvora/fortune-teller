import json_parser as jpar
import RetrievePrice as rp
import constants as ct
import datetime as dt
import pandas as pd
reload(jpar)

def main():
    companies = ['amazon','Cisco','IBM','Infosys','symantec','Visa']
    company_articles = {}          #Stores company and its corresponding article
    company_timestamp = {}         #Stores company and its corresponding timestamp
    parse_data = jpar.ParseData()

    # Get relevant data from json
    for company in companies:
        #print "Extracting articles from {0}".format(company)
        articles = parse_data.extractArticlesFromJSON('Data/{0}.json'.format(company),company)
        company_articles[company] = articles

    for key in company_articles:
        temp = []
        articles = company_articles[key]
        for article in articles:
            #res = str(article.timestamp) + "_" + article.date[:8]
            res = article.timestamp
            temp.append(res)
        company_timestamp[key] = temp

    #print company_timestamp

    # Get Stock Price for past 30 days
    rs = rp.RetrieveStockPrice(300, 60)
    res = rs.getStockPricesForCompanies(['amzn','CSCO','IBM','INFY','SYMC','V'])

    relevant_sp = {}
    for org in company_timestamp.keys():
        for ts in company_timestamp[org]:
            ts_converted = dt.datetime.fromtimestamp(ts)
            #y = res[ct._TICKERS[org]]
            #m = y[['ts']]
            print res[ct._TICKERS[org]]['ts']
            if ts_converted in res[ct._TICKERS[org]]['ts']:
                relevant_sp[org] = res[ct._TICKERS[org]]
    print relevant_sp


if __name__ == "__main__":
    main()
