import requests
import json


server_url = 'http://127.0.0.1:5000'
headers = {
'Accept': "multipart/form-data",
'Content-Type': "application/pdf",
'Cache-Control': "no-cache",
}

files2 = {
    'file': open('.\\test2.pdf', 'rb')
}
files = {
    'file': open('.\\test1.pdf', 'rb')
}

#2 Test Similar model
request = requests.post(server_url+ '/find_similar_article', json={"data": "article"}, files=files)
article = json.loads(request.text)
print("Most simular article(s) in base for article above:")
print(f"Titel {article['titel']}")
print(f"Pdf {article['pdflink']}")
print(f"Link {article['sitelink']}") 