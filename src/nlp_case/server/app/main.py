from flask import Flask, request, jsonify
import nltk
from nlp_case.server.app.models.text_keywords_models.TextRank_model import  TextRank_model
from nlp_case.server.app.models.text_keywords_models.Tfidf_model import Tfidf_model
from nlp_case.server.app.db.milvus_bridge import MilvusBridge
from nlp_case.server.app.models.parsers.PDFparser import Parser
from nlp_case.server.app.db.db_access import DBAccess
from nlp_case.server.app.models.Text_Similarity_model import Text_Similarity_model
from nlp_case.server.app.models.NER_Disease_recognizer import NERDiseaseRecognizer
from nlp_case.server.app.models.NER_Disease_net import SentenceDiseaseRecognizer, StackedConv1d
from waitress import serve
import re
import os


app = Flask(__name__)

<<<<<<< HEAD
=======
@app.route('/')
def hello_world():
    return 'NLP keyword/NER/text similarity project. Contact authors to get the API.'

>>>>>>> d547cb1b6bd478135572515a6ba2e18d91a3bb32
@app.route('/predict_keywords', methods=["POST"])
def predict():
    article = request.form.get("text")
    keywords = tf_model.predict_keywords(article)
    return jsonify({'result': keywords})

@app.route('/get_keywords', methods = ["GET"])
def get_keywords():
    if request.get_json() != None:
        pattern = request.get_json().get("pattern", "")
        number = request.get_json().get("number", 0)
    else:
        pattern = ""
        number = 0
    keywords = access.get_all_keywords()
    if pattern != "":
        keywords = list(filter(lambda w: re.search(pattern, w), keywords))
    if number > 0:
        keywords = keywords[:number]
    return jsonify({'result': keywords})

@app.route('/search_articles_with_keywords', methods=["POST"])
def find_by_keywords():
    keywords = request.get_json().get("keywords")
    papers = access.search_keywords(keywords, num_results=3)
    return jsonify({'result': 
    [{'title': p[0], 'pdf_link': p[3], 'site_link': p[2]} for p in papers]})

@app.route('/parse_pdf', methods=["POST"])
def parse_pdf():
    json_data = request.files["file"]
    res = Parser.get_text_from_pdf(json_data)
    return jsonify({'result': res})
    
@app.route('/find_similar_article', methods=["POST"])
def find_most_similar():
    json_data = request.files["file"]
    res = sim_model.find_similar_article(json_data)
    print(res)
    return jsonify({'title': res['title'],'sitelink': res['sitelink'], 'pdflink': res['pdflink']})

@app.route('/find_disease_names', methods=["POST"])
def find_dis_names():
    text = request.get_json().get("text")
    disease_entities = NER_model.find_all_Disease_entities(text)
    return jsonify({'diseases': disease_entities})

@app.route('/find_disease_names_in_file', methods=["POST"])
def find_dis_names_infile():
    file = request.files["file"]
    print(file.read())
    disease_entities = NER_model.find_all_Disease_entities([file.read().decode("utf-8")])
    return jsonify({'diseases': disease_entities})


if __name__ == '__main__':
    bridge = MilvusBridge()
    print(os.path.abspath(__file__))
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')
    NER_model = NERDiseaseRecognizer()
    access = DBAccess("7P7RRzvV516fhdQX")
    sim_model = Text_Similarity_model(access)
    tf_model = Tfidf_model(access.get_papers_iterator())
    serve(app, host="0.0.0.0", port="5000")
    

