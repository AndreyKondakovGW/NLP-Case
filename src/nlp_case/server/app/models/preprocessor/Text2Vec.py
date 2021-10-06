import pandas as pd
import numpy as np
from nlp_case.server.app.models.preprocessor.StandartPreprogressor import preprocess_text
import nltk
import gensim
from gensim.models import KeyedVectors

from collections import Counter
import itertools

#articles_df = pd.read_csv('./data/data.csv')
#clean_df = pd.DataFrame(data={"title": articles_df.iloc[:,0], "description": articles_df.iloc[:,1],"site_link":articles_df.iloc[:,2],"pdf_link": articles_df.iloc[:,3]})
#clean_df.to_csv('./data/clean_data.csv', index=True)

class MyText2VecModel:
    @staticmethod
    def save_embadding_model(filename):
        stopwords = nltk.corpus.stopwords.words("english")

        articles_df = pd.read_csv('./data/clean_data.csv')
        articles_df["clean_description"] = articles_df["description"].apply(lambda text: preprocess_text(text,stopwords=stopwords))

        corpus = articles_df["clean_description"]

        ## create list of lists of unigrams
        lst_corpus = []
        for string in corpus:
            lst_words = string.split()
            lst_grams = [" ".join(lst_words[i:i+1]) 
                for i in range(0, len(lst_words), 1)]
            lst_corpus.append(lst_grams)

        ## detect bigrams and trigrams
        '''bigrams_detector = gensim.models.phrases.Phrases(lst_corpus, 
                 delimiter=" ".encode(), min_count=5, threshold=10)
        bigrams_detector = gensim.models.phrases.Phraser(bigrams_detector)
        trigrams_detector = gensim.models.phrases.Phrases(bigrams_detector[lst_corpus], 
            delimiter=" ".encode(), min_count=5, threshold=10)
        trigrams_detector = gensim.models.phrases.Phraser(trigrams_detector)'''

        word_data = gensim.models.word2vec.Word2Vec(lst_corpus, vector_size=100,   
            window=5, min_count=1, sg=1)
        word_data.wv.save(filename)

    @staticmethod
    def generate_embadding(model_name, data_df):
        stopwords = nltk.corpus.stopwords.words("english")
        word_emb_model = KeyedVectors.load(model_name)
        data_df["clean_description"] = data_df["description"].apply(lambda text: preprocess_text(text,stopwords=stopwords))
        data = []
        for description in data_df["clean_description"]:
            embadding_vector = get_sif_feature_vector(description, word_emb_model)
            data.append(embadding_vector)
        embadding_df = pd.DataFrame(np.array(data),columns=range(100))
        embadding_df['description'] = data_df["description"]
        print(embadding_df.head())
        embadding_df.to_csv('./data/embadding_data.csv', index=True)

          

def map_word_frequency(document):
    return Counter(itertools.chain(*document))
    
def get_sif_feature_vector(text, word_emb_model):
    text = [token for token in text.split() if token in word_emb_model.index_to_key]
    word_counts = map_word_frequency((text))
    embedding_size = 100 # size of vectore in word embeddings
    a = 0.001
    for sentence in [text]:
        vs = np.zeros(embedding_size)
        sentence_length = len(sentence)
        for word in sentence:
            a_value = a / (a + word_counts[word]) # smooth inverse frequency, SIF
            vs = np.add(vs, np.multiply(a_value, word_emb_model[word])) # vs += sif * word_vector
        vs = np.divide(vs, sentence_length) # weighted average
        sentence_set = vs
    return sentence_set