import requests

data = {"keywords": ["math", "vision"]}
headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
request= requests.post("http://127.0.0.1:5000/search_articles_with_keywords", json=data, headers=headers)

print(request.text)