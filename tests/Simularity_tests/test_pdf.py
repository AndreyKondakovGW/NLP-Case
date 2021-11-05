import requests
import json


server_url = 'https://nlp-case-elia-morrison.cloud.okteto.net'
headers = {
'Accept': "multipart/form-data",
'Content-Type': "application/pdf",
'Cache-Control': "no-cache",
}

files2 = {
    'file': open('.\\test2.pdf', 'rb')
}
files = {
    'file': open('.\\test.pdf', 'rb')
}

#1 Test PDF parser
request = requests.post(server_url+ '/parse_pdf', json={"data": "article"}, files=files2)
jsonData = json.loads(request.text)
text = jsonData['result']
print("Text verson of PDF")
print(text)

print()
print()
files2 = {
    'file': open('.\\test2.pdf', 'rb')
}
#2 Test Similar model
request = requests.post(server_url+ '/find_similar_article', json={"data": "article"}, files=files2)
article = json.loads(request.text)
print("Most simular article(s) in base for article above:")
print(f"Title {article['title']}")
print(f"Pdf {article['pdflink']}")
print(f"Link {article['sitelink']}") 