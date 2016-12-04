#JSON file parser

import json
from objects import Article, StockPrice

def extractArticlesFromJSON(jsonFile):
    
    articles = []
    
    jsonData = open(jsonFile).read()
    
    # Create dictionary from json data
    data = json.loads(jsonData)

    # Extract docs object from the result object in data
    docs = data['result']['docs']

    for doc in docs:
        timestamp = doc['timestamp']
        title = doc['source']['enriched']['url']['title']
        #url = doc['source']['enriched']['url']['url']
        sentimentScore = doc['source']['enriched']['url']['docSentiment']['score']

        article = Article(title, timestamp, sentimentScore)
        articles.append(article)
    print len(articles)

extractArticlesFromJSON('Data/Test1.json')
