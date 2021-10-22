from nlp_case.server.app.models.preprocessor.StandartPreprogressor import preprocess_text, preprogress_corpus, tokenizer_regex, tokenize_corpus
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import pandas as pd
import nltk
import os

DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + "\..\..\..\data\clean_data.csv"

class Tfidf_model:
    def __init__(self, use_stopword = True):
        if (use_stopword):
            stopwords = nltk.corpus.stopwords.words("english")
            self.cv=CountVectorizer(max_df=0.8,stop_words=stopwords, ngram_range=(1,4))
            self.transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
        else:
            self.cv=CountVectorizer(max_df=0.8, ngram_range=(1,4))
            self.transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
        articles_df = pd.read_csv(DATA_PATH)
        clean_corpus = [' '.join(tokens) for tokens in tokenize_corpus(articles_df['description'].tolist(), tokenizer=tokenizer_regex, min_token_size=1)]
        clean_corpus = preprogress_corpus(clean_corpus)

        self.word_count_vector=self.cv.fit_transform(clean_corpus)
        self.transformer = self.transformer.fit(self.word_count_vector) 
        
    
    def predict_keywords(self, text, count = 5):
        clean_text = ' '.join(tokenizer_regex(text, min_token_size=1))
        clean_text = preprocess_text(clean_text)

        tf_idf_vector=self.transformer.transform(self.cv.transform([clean_text]))
        tuples = zip(tf_idf_vector.tocoo().col, tf_idf_vector.tocoo().data)
        sorted_items =  sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

        feature_names=self.cv.get_feature_names()
        sorted_items = sorted_items[:count]

        score_vals = []
        feature_vals = []
    
        for idx, score in sorted_items:
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])

        results= {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]]=score_vals[idx]
    
        return results


        
