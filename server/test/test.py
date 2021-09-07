import requests

with open('article.txt') as f:
    article_text = f.read()
data = {"titel":'Article',"body": article_text}
request= requests.post("http://127.0.0.1:5000/predict_keywords", data=data)

print(request.text)