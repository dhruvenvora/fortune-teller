#JSON file parser

import json
import objects as obj
import constants as ct
import RetrievePrice as rp
import datetime as dt

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
            #timestamp = doc['timestamp']
            # If the publication date is 2016 then process it, else skip
            if doc['source']['enriched']['url']['publicationDate']['date'][:4] == '2016':
                year = int(doc['source']['enriched']['url']['publicationDate']['date'][:4] )
                month = int(doc['source']['enriched']['url']['publicationDate']['date'][4:6] )
                day = int(doc['source']['enriched']['url']['publicationDate']['date'][6:8] )
                timestamp = int((dt.datetime(year,month,day,0,0) - dt.datetime(1970,1,1)).total_seconds())

                title = doc['source']['enriched']['url']['title']
                sentimentScore = doc['source']['enriched']['url']['docSentiment']['score']
                date = doc['source']['enriched']['url']['publicationDate']['date']
                article = obj.Article(title,timestamp,sentimentScore,date,ct._TICKERS[company])
                articles.append(article)
        return articles


