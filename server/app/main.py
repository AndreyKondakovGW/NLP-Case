from flask import Flask, request, jsonify
from models import TextRank_model
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'
@app.route('/predict_keywords', methods=["POST"])
def predict():
    title = request.form.get("title")
    article = request.form.get("body")
    print(request.form)
    keywords = model.predict_tags(article)
    return jsonify({'result': keywords})

if __name__ == '__main__':
    model = TextRank_model()
    app.run()

