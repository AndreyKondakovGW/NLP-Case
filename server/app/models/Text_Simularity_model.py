import pandas as pd
from gensim.models import KeyedVectors
import parsers
from preprocessor import get_sif_feature_vector, preprocess_text
import nltk
from sklearn.metrics.pairwise import cosine_similarity
def get_cosine_similarity(feature_vec_1, feature_vec_2):    
    return cosine_similarity(feature_vec_1.reshape(1, -1), feature_vec_2.reshape(1, -1))[0][0]

class Text_Simularity_model:
    def __init__(self, datapath, modelpath):
        self.data = pd.read_csv(datapath,index_col=False)
        self.model = KeyedVectors.load(modelpath)

    def find_similar_article(self,filename):
        stopwords = nltk.corpus.stopwords.words("english")
        parsers.Parser.parsePDF(filename)
        description = parsers.Parser.getDescription('./server/app/tmp/out.txt')
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


sim_model = Text_Simularity_model('./data/embadding_data.csv', './word2vec.wordvectors')
sim_model.find_similar_article('./test.pdf')