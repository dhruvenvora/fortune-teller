#Objects


# This class contains the details of an article with publication time. The class also maps to
# the list of stock prices.
class Article:
    
    def __init__(self, title, timestamp, sentimentScore, ticker):
        self.title = title
        self.timestamp = timestamp
        self.sentimentScore = sentimentScore
        self.ticker = ticker
        self.stockPrices = []

    def addStock(self, stockPrice):
        self.stocksPrices.append(stockPrice)


# This class stores the price imformarion of a stock at given time.
class StockPrice:

    def __init__(self, entity, price, timestamp):
        self.entity = entity
        self.price = price
        self.timestamp = timestamp
        self.article = None
    
    def mapArticle(self, article):
        self.article = article



