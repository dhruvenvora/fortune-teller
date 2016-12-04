import parser

def main():
    parse_data = parser.Parse_Data()
    parse_data.extractArticlesFromJSON('Data/Test1.json')
    
if __name__ == '__main__':
    main()