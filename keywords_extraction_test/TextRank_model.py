from summa import keywords as summa_keywords
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

class TextRank_model:
    def __init__(self, name="TextRank", lemmatize=False):
        self.name = name
        self.lemmatize = lemmatize
        self.stoplist = set(stopwords.words('english'))
        if lemmatize:
            self.lemmatizer = WordNetLemmatizer()
        

    def predict_tags(self, text):
        keywords = summa_keywords.keywords(text).split()
        
        if self.lemmatize:
            keywords = list({self.lemmatizer.lemmatize(kwrd) for kwrd in keywords})
        return keywords