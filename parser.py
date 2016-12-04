#JSON file parser

import json
from objects import Article, StockPrice
import constants as cts


class Parse_Data(object):

    def extractArticlesFromJSON(self, jsonFile):    
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
                Article(title,timestamp,sentimentScore,cts._TICKERS['amazon'])
            articles.append(article)
        print articles
