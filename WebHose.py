import time,os
import constants as ct
"""
import unirest

response = unirest.get("https://webhose.io/search?token=f9cf7cbd-5c93-4672-8cb0-f6da249d1808&format=json&q=amazon%20OR%20AMZN&sort=relevancy&ts=1478463348741",
    headers={
    "Accept": "text/plain"
    }
)

print response.body
"""

import webhose
webhose.config(token='f9cf7cbd-5c93-4672-8cb0-f6da249d1808')

company_list = ["PayPal"]
news_content = {}
for org in company_list:
    r = webhose.search(org)
    news_content[org] = {}
    articleNo = 1
    while True:
        for post in r:
            news_content[org][articleNo] = {}
            if post.language == 'english' and post.published[:4] == '2016':
                timestamp = post.published[:10] + post.published[11:19]
                news_content[org][articleNo][timestamp] = [ post.title, post.text ] 
                
                #filename = os.getcwd() + os.path.sep + ct._DATADICTIONARY + os.path.sep + '{0}.json'.format(org)
                #with open(filename,"a") as f:
                #    f.write(str(str(post.title) + str(timestamp) + str('*' * 25) + str(post.text)))
                
                print post.title,post.published
            
            articleNo += 1 
            
            if articleNo > 200:
                break
        time.sleep(300)
    
        r = r.get_next()

"""
r = webhose.search("skyrim")
while True:
    for post in r:
        perform_action(post)
    time.sleep(300)
    r = r.get_next()
"""