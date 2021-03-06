import requests
import os
import constants as ct
#import json
#from bs4 import BeautifulSoup

sentiments = 'any positive negative neutral'
sentiments = sentiments.split()

# types = 'free text company organization'
# types = types.split()
#api_key = "b277064a32f27ed4af54b1833a4ea8b6996ea07c" or "59b2ea1a1a004851635f43e0ce788b5bc92daca0"

#company_list = ["PayPal", "MapR", "Cisco", "Symantec", "Visa", "IBM", "Infosys", "Tesla"]
company_list = ["PayPal"]

def news_api(org,nextURL=''):
    url = 'https://access.alchemyapi.com/calls/data/GetNews?apikey={0}&return=enriched.url.title,enriched.' \
          'url.url,enriched.url.publicationDate,enriched.url.docSentiment&start=1477958400&end=1480550340&q.enriched.url.' \
          'entities.entity=|text={1},type=company|&q.enriched.url.taxonomy.taxonomy_.label=technology%20and%20computing&count=25&outputMode=json{2}'.format(ct._APIKEY,org,"&next="+nextURL)
    s = requests.get(url);
    return s


def writeToFile():

    for org in company_list:
        s = news_api(org)
        #print s.text
        filename = os.getcwd() + os.path.sep + ct._DATADICTIONARY + os.path.sep + '{0}.json'.format(org)
        with open(filename,"a") as f:
            f.write(str(s.text))
        print s.text
        print s['result']['next']
        """
        nextURL = s['result']['next']
        while nextURL:
            nextResult = news_api(org,nextURL)
            with open(filename,"a") as f:
                f.write(str(nextResult.text))
                nextURL = nextResult['result']['next']
        """


writeToFile()
#https://access.alchemyapi.com/calls/data/GetNews?apikey=YOUR_API_KEY_HERE&return=enriched.url.title,enriched.url.url,enriched.url.publicationDate,
#enriched.url.docSentiment&start=1480032000&end=1480719600&q.enriched.url.entities.entity=|text=facebook,
#type=company|&q.enriched.url.taxonomy.taxonomy_.label=technology%20and%20computing&count=25&outputMode=json
