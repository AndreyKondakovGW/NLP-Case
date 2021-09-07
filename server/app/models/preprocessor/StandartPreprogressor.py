import re
import nltk

def preprocess_text(text, stemm=False, lemm=True, stopwords=None):
    ## clean (convert to lowercase and remove punctuations and   
    ##characters and then strip)
    text = re.sub(r'[^\w\s\n]', '', str(text).lower().strip())
            
    ## Tokenize (convert from string to list)
    lst_text = text.split()
    ## remove Stopwords
    if stopwords is not None:
        lst_text = [word for word in lst_text if word not in 
                    stopwords]
                
    ## Stemming (remove -ing, -ly, ...)
    if stemm == True:
        ps = nltk.stem.porter.PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]
                
    ## Lemmatisation (convert the word into root word)
    if lemm == True:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]
            
    ## back to string from list
    text = " ".join(lst_text)
    return text