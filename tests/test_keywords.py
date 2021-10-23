import requests

data = {"keywords": ["math", "vision"]}
headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
request= requests.post("http://127.0.0.1:5000/search_articles_with_keywords", json=data, headers=headers)
print(request.text)


text = '''We consider the potential density of rational points on an algebraic variety

defined over a number field K, i.e., the property that the set of rational points of X becomes

Zariski dense after a finite field extension of K. For a non-uniruled projective variety with

an int-amplified endomorphism, we show that it always satisfies potential density. When

a rationally connected variety admits an int-amplified endomorphism, we prove that there

exists some rational curve with a Zariski dense forward orbit, assuming the Zariski dense

orbit conjecture in lower dimensions. As an application, we prove the potential density

for projective varieties with int-amplified endomorphisms in dimension ≤ 3. We also study

the existence of densely many rational points with the maximal arithmetic degree over a

sufficiently large number field.'''

'''data = {"body": text,
        "title": "Titel"}
request= requests.post("http://127.0.0.1:5000/predict_keywords", json=data, headers=headers)
print(request.text)'''