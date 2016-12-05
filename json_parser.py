#JSON file parser

import json
import objects as obj
import constants as ct
import RetrievePrice as rp

reload(obj)
reload(ct)
reload(rp)


class ParseData(object):
    
    def extractArticlesFromJSON(self, jsonFile,company):
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
            date = \
                 doc['source']['enriched']['url']['publicationDate']['date']
            article = \
                obj.Article(title,timestamp,sentimentScore,date,ct._TICKERS[company])
            articles.append(article)
        return articles


