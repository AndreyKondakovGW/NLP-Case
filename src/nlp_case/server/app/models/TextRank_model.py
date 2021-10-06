from summa import keywords as summa_keywords

class TextRank_model:
    def __init__(self, name="TextRank", lemmatize=False):
        self.name = name
        self.lemmatize = lemmatize

    def predict_tags(self,text):
        keywords = summa_keywords.keywords(text).split()
        return keywords