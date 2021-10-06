import pandas as pd
from gensim.models import KeyedVectors
from nlp_case.server.app.models.parsers.PDFparser import Parser
from nlp_case.server.app.models.preprocessor.StandartPreprogressor import preprocess_text
from nlp_case.server.app.models.preprocessor.Text2Vec import get_sif_feature_vector
import nltk
from sklearn.metrics.pairwise import cosine_similarity
import os

DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + "\..\..\..\data\embadding_data.csv"
MODEL_PATH = os.path.dirname(os.path.abspath(__file__)) + "\..\..\..\data\word2vec.wordvectors"

def get_cosine_similarity(feature_vec_1, feature_vec_2):    
    return cosine_similarity(feature_vec_1.reshape(1, -1), feature_vec_2.reshape(1, -1))[0][0]

class Text_Simularity_model:
    def __init__(self, datapath = DATA_PATH, modelpath = MODEL_PATH):
        self.data = pd.read_csv(datapath,index_col=False)
        self.model = KeyedVectors.load(modelpath)

    def find_similar_article(self,filename):
        stopwords = nltk.corpus.stopwords.words("english")
        Parser.parsePDF(filename)
        description = Parser.getDescription('./server/app/tmp/out.txt')
        print('Article description:')
        print(description)
        description_clean = preprocess_text(description, stopwords=stopwords)
        description_vector = get_sif_feature_vector(description_clean, self.model)

        distants = []
        for index, row in self.data.iterrows():
            vector = row.drop(['Unnamed: 0','description'])
            distants.append(get_cosine_similarity(description_vector, vector.to_numpy()))
        self.data['distant'] = pd.Series(data = distants)
        print('Most Similar article: ')
        res = self.data[self.data['distant'] == self.data['distant'].min()]
        print(res['description'].array[0])

