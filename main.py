import json_parser as jpar
import RetrievePrice as rp
import constants as ct
import datetime as dt
import os
from newspaper import Article
from aylienapiclient import textapi
import json
import urllib
import urllib2
import newspaper
reload(jpar)

APPLICATION_ID = "91ed28e0"
APPLICATION_KEY = "232d81bcc9f262539a8eefcbf92e50a6"

from nytimesarticle import articleAPI

def GetArchivesNYT(company, entities):
    print company, ':', entities
    api = articleAPI('d77682cbc8ff4c3b9b9c20c797f7dfb2')
    articles = api.search( q = entities, 
     fq = {'headline': company, 'source':['Reuters','AP','The New York Times',\
                'RETRO REPORT','Technology',' Amazon - Technology']}, 
     begin_date = 20160901 )
     
    news = []
    try:
        for i in articles['response']['docs']:
            dic = {}
            dic['date'] = i['pub_date'] # cutting time of day.
            dic['url'] = i['web_url']
            if dic['date'] is not None:
                news.append(dic)
    except:
        print 'Could not retrieve articles for ', company
        
    return news
    
def call_api(endpoint, parameters):
  url = 'https://api.aylien.com/api/v1/' + endpoint
  headers = {
      "Accept":                             "application/json",
      "Content-type":                       "application/x-www-form-urlencoded",
      "X-AYLIEN-TextAPI-Application-ID":    APPLICATION_ID,
      "X-AYLIEN-TextAPI-Application-Key":   APPLICATION_KEY
  }
  opener = urllib2.build_opener()
  request = urllib2.Request(url, urllib.urlencode(parameters), headers)
  response = opener.open(request);
  return json.loads(response.read())

def CreateGoogleNewsPaper():
    googlenews_paper = newspaper.build(u'https://news.google.com/')
        
    for google_article in googlenews_paper.articles:
        google_article.download()
        try:
            google_article.html
            google_article.parse()
            google_article.text
        except:
            continue
    
def news_org_api(articleurl):
    print articleurl
    try:
        article = Article(articleurl)
        article.download()
        parameters = {"text": article.text}
        sentiment = call_api("sentiment", parameters)
        print "Sentiment: %s (%F)" % (sentiment["polarity"], sentiment["polarity_confidence"])
    except:
        return
    #https://news.google.com/news/section?cf=all&topic=tc&ned=us&siidp=999617ba05c99a1f7cd55bc1d83a19906dda&ict=ln

def main():
    #Apple, Samsung, Google, 
    companies = {'Apple':['iphone','macbook'], 'Samsung':['mobile'],'Microsoft':['windows']}
    company_articles  = {}          #Stores company and its corresponding article
    company_timestamp = {}         #Stores company and its corresponding timestamp
    
    for company, entities in companies.items():
        try:
            company_articles[company] = GetArchivesNYT(company, entities) 
        except:
            print 'No information about ', company
            
    for company in company_articles.keys():
        print company 
        for value in company_articles[company]:
            news_org_api(value['url'])
            
    # Get Stock Price for past 60 days
    rs = rp.RetrieveStockPrice(300, 60)
    res = rs.getStockPricesForCompanies(['amzn','CSCO','IBM','INFY','SYMC','V'])
    print "\nPrinting Stock prices : %s" % (res)
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
