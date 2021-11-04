from nlp_case.server.app.models.preprocessor.StandardPreprocessor import preprocess_text, preprocess_corpus, tokenizer_regex, tokenize_corpus
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pandas as pd
import nltk
import os
import pickle

DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + "\..\..\..\..\data\clean_data.csv"
TFIDF_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../../../../data/tfidf.pkl" #LOL
COUNTVEC_PATH = os.path.dirname(os.path.abspath(__file__)) + "/../../../../data/countvec.pkl"

class Tfidf_model:
    def __init__(self, data_iterator, use_stopwords=True):
        print("Initializing Tfidf_model...")
        if os.path.exists(COUNTVEC_PATH) and os.path.exists(TFIDF_PATH):
            self.transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
            vocabulary = pickle.load(open(COUNTVEC_PATH, "rb"))
            if use_stopwords:
                stopwords = nltk.corpus.stopwords.words("english")
                self.cv = CountVectorizer(max_df=0.5, stop_words=stopwords, ngram_range=(1,2), vocabulary=vocabulary)
            else:
                self.cv=CountVectorizer(max_df=0.5, ngram_range=(1,2), vocabulary=vocabulary)
                
            idf = pickle.load(open(TFIDF_PATH, "rb"))
            self.transformer.idf_ = idf
        else:
            self._fit_new_model(data_iterator, use_stopwords=use_stopwords)
        
    def _fit_new_model(self, data_iterator, use_stopwords=True):
        print("Fitting new Tfidf_model...")
        if (use_stopwords):
            stopwords = nltk.corpus.stopwords.words("english")
            self.cv = CountVectorizer(max_df=0.5, stop_words=stopwords, ngram_range=(1,2))
            self.transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
        else:
            self.cv = CountVectorizer(max_df=0.5, ngram_range=(1,2))
            self.transformer = TfidfTransformer(smooth_idf=True,use_idf=True)

        #again loads the whole DB in RAM, needs a fix
        clean_corpus = []
        for paper in data_iterator:
            text = paper['abstract']
            text = preprocess_text(text)
            text = ' '.join(tokenizer_regex(text, min_token_size=3))
            clean_corpus.append(text)

        self.word_count_vector=self.cv.fit_transform(clean_corpus)
        self.transformer = self.transformer.fit(self.word_count_vector) 
        
        pickle.dump(self.cv.vocabulary_, open(COUNTVEC_PATH, "wb"))
        pickle.dump(self.transformer.idf_, open(TFIDF_PATH, "wb"))
    
    def predict_keywords(self, text, num_keywords=10):
        clean_text = preprocess_text(text)
        clean_text = ' '.join(tokenizer_regex(clean_text, min_token_size=3))

        tf_idf_vector=self.transformer.transform(self.cv.transform([clean_text]))
        tuples = zip(tf_idf_vector.tocoo().col, tf_idf_vector.tocoo().data)
        sorted_items =  sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

        feature_names=self.cv.get_feature_names()
        sorted_items = sorted_items[:num_keywords]

        #score_vals = []
        feature_vals = []
    
        for idx, score in sorted_items:
            #score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])

        #results= {}
        #for idx in range(len(feature_vals)):
        #    results[feature_vals[idx]]=score_vals[idx]
    
        return feature_vals


        
