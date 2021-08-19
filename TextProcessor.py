import urllib.request as libreq
import xml.etree.ElementTree as ET
import csv
import re
import numpy as np
import random
import os
from operator import itemgetter
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.text import TextCollection
from sklearn.feature_extraction.text import TfidfVectorizer

class TextProcessor:
    """
    Class responsible for main functionality
    
    Attributes
    ----------
    corpus : list
        main corpus of papers. 
        each entry is in format ["title","abstract","sitelink","pdflink"]
    
    """
    def __init__(self, filename, num_papers):
        """
        Initializes self.corpus from filename (csv),
        randomly selecting num_papers from all papers in csv.
        If csv is too small, throws exception
        
        Parameters
        ----------
        filename : str
            path to csv. Should be of the following structure:
            "title","abstract","sitelink","pdflink"
        num_papers : int
            number of papers to select from csv
            
        Raises
        ------
        ValueError
            If num_papers < rows of csv
        """
        with open(filename, 'r', encoding = 'utf-8') as textfile:
            csvreader = csv.reader(textfile, delimiter=',', quotechar='"')
            
            num_rows = sum(1 for row in csvreader)
            textfile.seek(0)
            if (num_rows < num_papers):
                raise ValueError("num_papers > number of rows in the csv file!")
            
            samples = sorted(random.sample(range(num_rows), num_papers))
            self.corpus = []
            
            maxind = len(samples)
            j = 0
            for i, row in enumerate(csvreader):
                if (i == samples[j]):
                    self.corpus.append([row[0].replace(r'\n', '\n'), 
                        row[1].replace(r'\n', '\n'), row[2], row[3]])
                    j += 1
                    if (j >= maxind):
                        break
    
    @staticmethod
    def download_papers(filename, filemode = 'w', num_papers = 30000, 
        start_ind = 0, step = 100, search_query = None, verbose = True):
        """
        Downloads papers from arxiv.org, OVERWRITING filename (csv), if filemode is not supplied
        Is extremely slow (may take a WEEK to download ~million of papers), 
        due to broken API of arxiv.
        TODO: write a workaround for larger amounts of papers
        
        Parameters
        ----------
        filename : str
            where .csv is saved
        filemode : str
            standard python file mode (e.g. 'a' for append and 'w' to overwrite)
        num_papers : int
            number of papers to download, expect difficulties when downloading > 30000 at once.
            (again an API restriction)
        start_ind : int
            paper to start from (i.e. how many papers we skip at the beginning of a query)
        step : int
            number of papers to download in one query. should be < 2000 (API restriction) 
            better leave as default. when experiencing troubles downloading, use step = 10.
            step = 1000 works best, but inconsistently
        search_query : string
            an actual search request to the server. https://arxiv.org/help/api/user-manual#_query_interface
        verbose : bool
        """
        base_url = 'http://export.arxiv.org/api/query?'
        #allows to obtain the entire database of english papers (around 1.9M, only ~100 are missing in total) through only 1 query
        
        if not search_query:
            search_query = ('all:the+all:a+all:to+all:and+all:of+'
                            'all:in+all:with+all:has+all:be+all:its+'
                            'all:for+all:at+all:that+all:on+all:this')
                        
        namespace = '{http://www.w3.org/2005/Atom}' #namespace in an XML document
        
        with open(filename, filemode, newline='', encoding="utf8") as csvfile:
            csvwriter = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)
            received = 0
            for start in range(start_ind, num_papers+start_ind, step):
                query = 'search_query=%s&start=%i&max_results=%i' % (search_query,
                                                                 start,
                                                                 step)

                entries = ''
                while not len(entries) == step:
                    if not entries == '' and verbose: #if we're not on the first iteration
                        print('Failed to receive correct response! Number of entries: ' + str(len(entries)))
                    response = libreq.urlopen(base_url + query).read().decode('utf-8')
                    root = ET.fromstring(response)
                    entries = root.findall(namespace + 'entry')

                for entry in entries:
                    title =  entry[3].text
                    abstract = entry[4].text
                    pdflink, sitelink = '', ''
                    for link in entry.findall(namespace + 'link'): 
                        if link.attrib.get('title') == 'pdf': #see https://arxiv.org/help/api/user-manual#entry_links
                            pdflink = link.attrib.get('href')
                        elif not 'title' in link.attrib:
                            sitelink = link.attrib.get('href')

                    csvwriter.writerow([i.replace("\n",r"\n").replace("\t",r"\t").replace('"','') for i in [title, abstract, sitelink, pdflink]])
                    received += 1

                if verbose:
                    print(str(received) + '/' + str(num_papers) + ' done! Sent requests for: ' + str(start+step))
                    
    @staticmethod
    def extract_keywords(texts, max_keywords, relative = False, alg = 'tfidf-max', params = None):
        """
        Extracts keywords from a collection of texts (preprocessed)
        
        Parameters
        ----------
        texts : list
            list of strings to estimate keywords from
        max_keywords: number
            number of keywords if relative = False,
            ration between keywords and unique words in text if relative = True
        relative : bool
            see max_keywords
        alg : string
            what algorithm to use
        params : dict
            additional parameters for selected algorithm
            
        Returns
        -------
        list
            list of numpy ndarrays, (array of keywords for each element in list of texts)
        """
        
        if not params:
            params = {}
        
        if alg == 'tfidf-max':        
        
            vectorizer = params.get('vectorizer', 
                TfidfVectorizer(tokenizer = lambda x: x, lowercase=False))

            tfidf = vectorizer.fit_transform(texts)
            keywords = []
            features = np.array(vectorizer.get_feature_names())
            for row in range(tfidf.shape[0]):
                sl = slice(tfidf.indptr[row], tfidf.indptr[row+1])
                pairs = zip(tfidf.indices[sl], tfidf.data[sl])
                #maybe it's a bad practice to sort all elements while we need only n max
                #TODO: fix or decide to leave as is
                sorted_pairs = sorted(pairs, key = itemgetter(1), reverse = True)
                num_keywords = None
                
                if relative:
                    num_keywords = int(len(sorted_pairs) * max_keywords)
                else:
                    num_keywords = max_keywords
                    
                subscript = len(sorted_pairs) if num_keywords > len(sorted_pairs) else num_keywords
                keywords_ind = [i[0] for i in sorted_pairs[:subscript]]
                keywords.append(features[keywords_ind])
                
            return keywords
        else:
            raise NotImplementedError("This algorithm is not not implemented!")
            
    @staticmethod
    def compare_keywords(x, y):
        """
        Computes precision and recall for two sets of keywords
        
        Parameters
        ----------
        x : list
        y : list
            correct keywords
            
        Returns
        -------
        precision : float
        recall : float
        """
        intersection = [t for t in x if t in y]
        precision = len(intersection)/len(y)
        recall = len(intersection)/len(x)
        
        return precision, recall
            
    @staticmethod
    def filter(texts):
        """
        Filters texts, leaving them in string format
        
        Parameters
        ----------
        texts : list
        """
        regexes = [r'\$.*?\$', # removes all LATEX-formulas
                    r'[\W_]+', # removes all non-alphanumeric characters
                    r'(\b(\w*[^a-zA-z\s]+\w*)\b)|(\b\w{1}\b)',] #removes all 1-symbol words
                    #and words containing non-english symbols
        result = []
        for text in texts:
            for regex in regexes:
                text = re.sub(regex, ' ', text)
                
            text = ' '.join(text.split()) #TODO: remove this. it's here for aesthetic purposes during debug
            result.append(text)
        return result
        
    @staticmethod
    def preprocess(texts, stoplist = set(stopwords.words('english')),
                use_tag_prediction = True):
        """
        Tokenization, lemmatization
        
        Parameters
        ----------
        texts : list
        stoplist : set
        use_tag_prediction : bool
            whether to use nltk.pos_tag to predict part of speech of a given word.
            efficiency is unknown. slows down the process by A LOT.
            
        Returns
        -------
        list
            list of lists (list of words for each entry in texts)
        """
        
        def decode_tag(tag):
            #Map POS tag to first character lemmatize() accepts
            tag = tag[0].upper()
            tag_dict = {"J": wordnet.ADJ,
                        "N": wordnet.NOUN,
                        "V": wordnet.VERB,
                        "R": wordnet.ADV}
            return tag_dict.get(tag, wordnet.NOUN)
        
        lemmatizer = WordNetLemmatizer()
        result = []
        for text in texts:
            text = text.lower()
            tokens = word_tokenize(text)
            
            lem = None
            if use_tag_prediction:
                tags = nltk.pos_tag(tokens)
                lem = [lemmatizer.lemmatize(kv[0], decode_tag(kv[1])) for kv in tags if kv[0] not in stoplist]
            else:
                lem = [lemmatizer.lemmatize(t) for t in tokens if t not in stoplist]
                
            result.append(lem)
        
        return result
            
        