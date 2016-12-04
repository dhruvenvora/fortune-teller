import json_parser as jpar
reload(jpar)

def main():
    parse_data = jpar.ParseData()
    parse_data.extractArticlesFromJSON('Data/amazon.json')
    
if __name__ == "__main__":
    main()