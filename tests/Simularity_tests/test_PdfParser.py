import requests
import json


server_url = 'http://127.0.0.1:5000'
headers = {
'Accept': "multipart/form-data",
'Content-Type': "application/pdf",
'Cache-Control': "no-cache",
}

files2 = {
    'file': open('.\\test1.pdf', 'rb')
}

#1 Test PDF parser
request = requests.post(server_url+ '/parse_pdf', json={"data": "article"}, files=files2)
jsonData = json.loads(request.text)
text = jsonData['result']
print("Text verson of PDF")
print(text)