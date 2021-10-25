import re
import nltk

SIMPLE_RE_DIGIT = re.compile(r'[\w\d]+', re.I)
SIMPLE_RE = re.compile(r'[\w]+', re.I)

def tokenizer_regex(txt,to_lower=True, min_token_size=4):
    if (to_lower):
        txt = txt.lower()
    all_tokens = SIMPLE_RE.findall(txt)
    return [token for token in all_tokens if len(token) >= min_token_size]

def tokenize_corpus(texts, tokenizer, **tokenizer_kwargs):
    return [tokenizer(txt, **tokenizer_kwargs) for txt in texts]

def preprocess_corpus(texts, stemm=False, lemm=True, stopwords=None):
    return [preprocess_text(text, stemm=stemm, lemm=lemm, stopwords=stopwords) for text in texts]

def preprocess_text(text, stemm=False, lemm=True, stopwords=None):
    regex1 = r'\$.*?\$' # removes all LATEX-formulas
    regex2 = r'(\b(\w*\d+\w*)\b)|(\b\w{1}\b)' #removes all 1-symbol words and words containing numbers
    text = re.sub(regex1, ' ', text)
    text = re.sub(regex2, ' ', text)

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