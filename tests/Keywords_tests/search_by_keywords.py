import requests
import json

server_url = 'https://nlp-case-elia-morrison.cloud.okteto.net/'
headers = {'Content-Type': 'application/json', 'Accept':'application/json'}

#Test function of searching articles by keywords
#1 Geting all base's keywords
request = requests.get(server_url+ '/get_keywords')
jsonData = json.loads(request.text)
keywords = jsonData['result']
print(f'Nuber of keywords in base: ', {len(keywords)})
print()
print("First 100 keywords")
print(keywords[:100])

#2 Geting 50 keywords staarting with v
request = requests.get(server_url+ '/get_keywords', json = {"pattern": r'^v\w+\b', "number": 50}, headers=headers)
print("Geting 50 keywords staarting with v")
jsonData = json.loads(request.text)
keywords = jsonData['result']
print(keywords)

#3 Searching articels by keywords
data = {"keywords": ["math", "vision"]}
request= requests.post("https://nlp-case-elia-morrison.cloud.okteto.net//search_articles_with_keywords", json=data, headers=headers)
jsonData = json.loads(request.text)
for i,atr in enumerate(jsonData['result']):
    print(f"Article {i}:")
    print(f"Title {atr['title']}")
    print(f"Pdf {atr['pdf_link']}")
    print(f"Link {atr['site_link']}") 