from flask import Flask, request, jsonify
from nlp_case.server.app.models import TextRank_model
from nlp_case.server.app.db.db_access import DBAccess
from nlp_case.server.app.models.Text_Simularity_model import Text_Simularity_model
from nlp_case.server.app.models.NER_Disease_recognizer import NERDiseaseRecognizer
from nlp_case.server.app.models.NER_Disease_net import SentenceDiseaseRecognizer, StackedConv1d
import os

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/predict_keywords', methods=["POST"])
def predict():
    title = request.form.get("title")
    article = request.form.get("body")
    keywords = model.predict_tags(article)
    return jsonify({'result': keywords})


@app.route('/search_articles_with_keywords', methods=["POST"])
def find_by_keywords():
    keywords = request.get_json().get("keywords")
    papers = acsess.search_keywords(keywords, num_results=3)
    for p in papers:
        print(p[1])
        print()
        print('-' * 10)
        print()
    return jsonify({'result': 
    [{'titel': p[0], 'abstract': p[1]} for p in papers]})

    
@app.route('/find_similar_article', methods=["POST"])
def find_most_similar():
    json_data = request.files["file"]
    sim_model.find_similar_article(json_data)
    return jsonify({'result': 0})
@app.route('/find_disease_names', methods=["POST"])
def find_dis_names():
    text = request.get_json().get("text")
    disease_entities = NER_model.find_all_Disease_entities(text)
    return jsonify({'result': disease_entities})

if __name__ == '__main__':
    print(os.path.abspath(__file__))
    sim_model = Text_Simularity_model()
    acsess = DBAccess("7P7RRzvV516fhdQX")
    model = TextRank_model()
    NER_model = NERDiseaseRecognizer()
    app.run()

