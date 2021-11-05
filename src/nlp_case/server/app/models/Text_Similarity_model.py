import pandas as pd
from gensim.models import KeyedVectors
from nlp_case.server.app.models.parsers.PDFparser import Parser
from nlp_case.server.app.models.preprocessor.Text2Vec import MyText2VecModel
from nlp_case.server.app.models.preprocessor.StandardPreprocessor import preprocess_text
from nlp_case.server.app.models.preprocessor.Text2Vec import get_sif_feature_vector
from nlp_case.server.app.db.milvus_bridge import MilvusBridge
from nlp_case.server.app.models.preprocessor.custom_stopwords import custom_stopwords
import nltk
from sklearn.metrics.pairwise import cosine_similarity
import os


DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../../../data/embedding_data.csv"
MODEL_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../../../data/word2vec.wordvectors"

def get_cosine_similarity(feature_vec_1, feature_vec_2):    
    return cosine_similarity(feature_vec_1.reshape(1, -1), feature_vec_2.reshape(1, -1))[0][0]

class Text_Similarity_model:
    def __init__(self, db_access, datapath = DATA_PATH, modelpath = MODEL_PATH):
        uninitialized = False
        if not os.path.exists(modelpath): 
            uninitialized = True
            print('Waiting for creating the model')
            self.model = MyText2VecModel.save_embedding_model(modelpath, db_access.get_papers_iterator())
            print('Model was created')
        self.model = KeyedVectors.load(modelpath)
        if uninitialized:
            print('Waiting for creating the embedding')
            MyText2VecModel.generate_embedding(self.model, datapath, db_access.get_papers_iterator())
            print('Embedding was created')

        self.db_access = db_access
        self.db_access = db_access
        self.milvus = MilvusBridge()

    def find_similar_article(self, data):
        stopwords = custom_stopwords
        description = Parser.get_description_from_pdf(data)
        print('Article description:')
        print(description)
        description_clean = preprocess_text(description, stopwords=stopwords)
        description_vector = get_sif_feature_vector(description_clean, self.model)

        print('Most Similar article: ')
        _id = self.milvus.find_similar(description_vector, num_results=10)[0]
        paper = self.db_access.get_paper_by_id(_id)
        return paper
