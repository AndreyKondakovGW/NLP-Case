from nlp_case.server.app.models.parsers.tokenParser import tokenize_corpus
from nlp_case.server.app.models.NER_Disease_recognizer import NERDiseaseRecognizer
from nlp_case.server.app.models.NER_Disease_net import SentenceDiseaseRecognizer, StackedConv1d
import requests

test_sentences = [
    'A common human skin tumour is caused by activating mutations in beta-catenin.',
    'HFE mutations analysis in 711 hemochromatosis probands: evidence for S65C implication in mild form of hemochromatosis.',
    'Germline BRCA1 alterations in a population-based series of ovarian cancer cases.',
    'The rare form of the Q356R polymorphism was significantly (P = 0. 03) associated with a family history of ovarian cancer, suggesting that this polymorphism may influence ovarian cancer risk.',
    'Identification of APC2, a homologue of the adenomatous polyposis coli tumour suppressor.',
    'GCH1 mutation in a patient with adult-onset oromandibular dystonia.',
    'The hereditary hemochromatosis protein, HFE, specifically regulates transferrin-mediated iron uptake in HeLa cells.',
]
test_sentences2 = ['''We consider the potential density of rational points on an algebraic variety
defined over a number field K, i.e., the property that the set of rational points of X becomes
Zariski dense after a finite field extension of K. For a non-uniruled projective variety with
an int-amplified endomorphism, we show that it always satisfies potential density.''']
test_sentences_tokenized = tokenize_corpus(test_sentences, min_token_size=1)
sentences_word_recognizer = NERDiseaseRecognizer()

url = "http://127.0.0.1:5000/find_disease_names"
data = {"text": test_sentences}
headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
request= requests.post(url, json=data, headers=headers)


url = "http://127.0.0.1:5000/find_disease_names_in_file"
files = {
    'file': open('.\\test_NER.txt', 'rb')
}
r = requests.post(url, json={"data": "text_file"}, files=files)
print(request.text)
