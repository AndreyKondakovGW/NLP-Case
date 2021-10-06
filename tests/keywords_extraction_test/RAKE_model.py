from rake_nltk import Rake
from TextPreparator import lemmatize_text


class RAKE_model:
    def __init__(self, stopwords, max_length, name="RAKE", lemmatize=False):
        self.stopwords = stopwords
        self.name = name
        self.lemmatize = lemmatize
        self.model = Rake(
            punctuations=",.\"\'()[]:; ",
            stopwords=self.stopwords,
            max_length=max_length
        )
    def predict_tags(self,text):
        if (self.lemmatize):
            text = lemmatize_text(text)
        self.model.extract_keywords_from_text(text)
        keywords = self.model.get_ranked_phrases()
        return keywords
