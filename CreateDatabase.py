#Author: Salil Shenoy

from nytimesarticle import articleAPI
from newspaper import Article
import constants
import json
import urllib
import urllib2
import newspaper


class CreateDatabase(object):
    
    def __init__(self):
        self.api = articleAPI(constants.NYT_KEY)
    
    def GetArchivesNYT(self, company, entities):
        api = articleAPI(constants.NYT_KEY)
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
    
    def call_api(self, endpoint, parameters):
        url = 'https://api.aylien.com/api/v1/' + endpoint
        headers = {
            "Accept":                             "application/json",
            "Content-type":                       "application/x-www-form-urlencoded",
            "X-AYLIEN-TextAPI-Application-ID":    constants.APPLICATION_ID,
            "X-AYLIEN-TextAPI-Application-Key":   constants.APPLICATION_KEY
        }
        opener = urllib2.build_opener()
        request = urllib2.Request(url, urllib.urlencode(parameters), headers)
        response = opener.open(request);
        return json.loads(response.read())

    def CreateGoogleNewsPaper(self):
        googlenews_paper = newspaper.build(u'https://news.google.com/')            
        for google_article in googlenews_paper.articles:
            google_article.download()
            try:
                google_article.html
                google_article.parse()
                google_article.text
            except:
                continue
    
    def news_org_api(self, articleurl):
        try:
            article = Article(articleurl)
            article.download()
            parameters = {"text": article.text}
            sentiment = self.call_api("sentiment", parameters)
            print "Sentiment: %s (%F)" % (sentiment["polarity"], sentiment["polarity_confidence"])
        except:
            return
    
    def parse_articles(self, articles):
        '''
        This function takes in a response to the NYT api and parses
        the articles into a list of dictionaries
        '''
        news = []
        for i in articles['response']['docs']:
            dic = {}
            dic['date'] = i['pub_date']
            dic['url'] = i['web_url']   
            news.append(dic)
        return(news)
    
    def get_articles(self,date,query):
        '''
        This function accepts a year in string format (e.g.'1980')
        and a query (e.g.'Amnesty International') and it will 
        return a list of parsed articles (in dictionaries)
        for that year.
        '''
        all_articles = []
        for i in range(0,100): #NYT limits pager to first 100 pages. But rarely will you find over 100 pages of results anyway.
            articles = self.api.search(q = query,
                fq = {'source':['Reuters','AP', 'The New York Times']},
                begin_date = date + '0101',
                end_date = date + '1231',
                sort='oldest',
                page = str(i))
            articles = self.parse_articles(articles)
            all_articles = all_articles + articles
        return(all_articles)
    
    def createdb(self):
        Amnesty_all = []
        for i in range(2015,2016):
            print 'Processing' + str(i) + '...'
            Amnesty_year =  self.get_articles(str(i),'Amnesty International')
            Amnesty_all = Amnesty_all + Amnesty_year
