import json_parser as jpar
import RetrievePrice as rp
reload(jpar)

def main():
    #parse_data = jpar.ParseData()
    #parse_data.extractArticlesFromJSON('Data/amazon.json')
    
    rs = rp.RetrieveStockPrice(600, 2)
    print rs.getStockPricesForCompanies(['amzn', 'infy'])

if __name__ == "__main__":
    main()
