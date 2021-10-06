from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from TextPreparator import lemmatize_text
from sklearn.metrics.pairwise import cosine_similarity

class BERT_model:
    def __init__(self, name="BERT",n_gram_range = (1, 1), lemmatize=False):
        self.name = name
        self.n_gram_range = n_gram_range
        self.lemmatize = lemmatize

    def predict_tags(self,text):
        if (self.lemmatize):
            text = lemmatize_text(text)
        count = CountVectorizer(ngram_range=self.n_gram_range, stop_words="english").fit([text])
        candidates = count.get_feature_names()
        model = SentenceTransformer('distilbert-base-nli-mean-tokens')
        doc_embedding = model.encode([text])
        candidate_embeddings = model.encode(candidates)

        top_n = 10
        distances = cosine_similarity(doc_embedding, candidate_embeddings)
        keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]
        return keywords