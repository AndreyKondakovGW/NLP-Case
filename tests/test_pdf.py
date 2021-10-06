import requests

data = {}
url = "http://127.0.0.1:5000/find_similar_article"
files = {
    'data' : data,
    'document': open('./tests/test.pdf', 'rb')
}

headers = {
'Accept': "multipart/form-data",
'Content-Type': "application/pdf",
'Cache-Control': "no-cache",
}

r = requests.post(url, files=files, headers=headers)