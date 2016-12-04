#JSON file parser

import json
import objects as obj
import constants as ct
import RetrievePrice as rp

reload(obj)
reload(ct)
reload(rp)


class ParseData(object):
    
    def __init__(self):
        print 'CTOR Parse Data'

    def extractArticlesFromJSON(self, jsonFile): 
        print 'Am I here'   
        articles = []    
        jsonData = open(jsonFile).read()    
        # Create dictionary from json data
        data = json.loads(jsonData)
        # Extract docs object from the result object in data
        docs = data['result']['docs']

        for doc in docs:
            timestamp = doc['timestamp']
            title = doc['source']['enriched']['url']['title']
            sentimentScore = \
                doc['source']['enriched']['url']['docSentiment']['score']
            article = \
                obj.Article(title,timestamp,sentimentScore,ct._TICKERS['amazon'])
            articles.append(article)
        
        retrieve_price = rp.RetrieveStockPrice()
        print retrieve_price.get_google_data('AMZN', 300, 10)
