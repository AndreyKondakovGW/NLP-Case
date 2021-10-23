import requests

url = "http://127.0.0.1:5000/find_similar_article"
files = {
    'file': open('.\\test2.pdf', 'rb')
}

headers = {
'Accept': "multipart/form-data",
'Content-Type': "application/pdf",
'Cache-Control': "no-cache",
}

print(url)
r = requests.post(url, json={"data": "article"}, files=files)
print(r.text)