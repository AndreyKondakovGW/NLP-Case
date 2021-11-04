import pandas as pd
from gensim.models import KeyedVectors
from nlp_case.server.app.models.parsers.PDFparser import Parser
from nlp_case.server.app.models.preprocessor.Text2Vec import MyText2VecModel
from nlp_case.server.app.models.preprocessor.StandardPreprocessor import preprocess_text
from nlp_case.server.app.models.preprocessor.Text2Vec import get_sif_feature_vector
import nltk
from sklearn.metrics.pairwise import cosine_similarity
import os


DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + "\..\..\..\data\embedding_data.csv"
MODEL_PATH = os.path.dirname(os.path.abspath(__file__)) + "\..\..\..\data\word2vec.wordvectors"

def get_cosine_similarity(feature_vec_1, feature_vec_2):    
    return cosine_similarity(feature_vec_1.reshape(1, -1), feature_vec_2.reshape(1, -1))[0][0]

class Text_Similarity_model:
    def __init__(self, db_access, datapath = DATA_PATH, modelpath = MODEL_PATH):
        if not os.path.exists(modelpath): 
            print('Waiting for creating the model')
            self.model = MyText2VecModel.save_embedding_model(modelpath, db_access.get_papers_iterator())
            print('Model was created')
        self.model = KeyedVectors.load(modelpath)
        if not os.path.exists(datapath):
            print('Waiting for creating the embedding')
            MyText2VecModel.generate_embedding(self.model, datapath, db_access.get_papers_iterator())
            print('Embedding was created')

        self.db_access = db_access
        self.data = pd.read_csv(datapath,index_col=False)
        self.db_access = db_access


    def find_similar_article(self, data):
        stopwords = nltk.corpus.stopwords.words("english")
        description = Parser.get_description_from_pdf(data)
        print('Article description:')
        print(description)
        description_clean = preprocess_text(description, stopwords=stopwords)
        description_vector = get_sif_feature_vector(description_clean, self.model)

        distants = []
        for index, row in self.data.iterrows():
            vector = row.drop(['Unnamed: 0','_id'])
            distants.append(get_cosine_similarity(description_vector, vector.to_numpy()))
        self.data['distant'] = pd.Series(data = distants)
        print('Most Similar article: ')
        res = self.data[self.data['distant'] == self.data['distant'].min()]
        _id = res['_id'].array[0]
        paper = self.db_access.get_paper_by_id(_id)
<<<<<<< HEAD
        return paper
=======
        return paper
>>>>>>> c61f1e55eb7c626906c45f17c4f9eb677661eb5b
