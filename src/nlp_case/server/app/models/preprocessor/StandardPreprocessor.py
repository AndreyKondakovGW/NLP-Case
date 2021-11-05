import re
import nltk
from nltk.corpus import wordnet

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
    
#Map POS tag to first character lemmatize() accepts
def decode_tag(tag):
    if not hasattr(decode_tag, "tag_dict"):
        decode_tag.tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    
    tag = tag[0].upper()
    return decode_tag.tag_dict.get(tag, wordnet.NOUN)

def preprocess_text(text, stemm=False, lemm=True, stopwords=None, predict_tags=False):
    regex1 = r'\$.*?\$' # removes all LATEX-formulas
    regex2 = r'(\b(\w*\d+\w*)\b)|(\b\w{1}\b)' #removes all 1-symbol words and words containing numbers
    regex3 = r'\w*_\w*' #removes all words containing underscores
    text = re.sub(regex1, '', text)
    text = re.sub(regex2, '', text)
    text = re.sub(regex3, '', text)

    ## clean (convert to lowercase and remove punctuations and   
    ##characters and then strip)
    text = re.sub(r'[^\w\s\n]', '', str(text).lower().strip())
            
    ## Tokenize (convert from string to list)
    lst_text = nltk.word_tokenize(text)
                
    ## Stemming (remove -ing, -ly, ...)
    if stemm == True:
        ps = nltk.stem.porter.PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]
                
    ## Lemmatisation (convert the word into root word)
    if lemm == True:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        if predict_tags:
            tags = nltk.pos_tag(lst_text)
            lst_text = [lem.lemmatize(kv[0], decode_tag(kv[1])) for kv in tags]
        else:
            lst_text = [lem.lemmatize(word) for word in lst_text]
            
    ## remove Stopwords
    if stopwords is not None:
        lst_text = [word for word in lst_text if word not in 
                    stopwords]
            
    ## back to string from list
    text = " ".join(lst_text)
    return text