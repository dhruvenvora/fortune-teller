import json_parser as jpar
reload(jpar)

def main():
    print 'In main'
    parse_data = jpar.ParseData()
    parse_data.extractArticlesFromJSON('Data/Test1.json')
    
if __name__ == "__main__":
    main()