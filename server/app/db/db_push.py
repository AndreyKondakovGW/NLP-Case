import pymongo
from keywords_extraction_test.TextRank_model import TextRank_model

class DBPusher:
    """
    class to populate the entire database with new data.
    all previous data should be erased
    """
    
    def __init__(self, pwd):
        self.client = pymongo.MongoClient("mongodb+srv://nlp_admin:"+pwd+"@cluster0.oelvn.mongodb.net/Cluster0?retryWrites=true&w=majority")
        self.db = self.client.nlp
        
    def _get_collection(self, collection)
        collections = self.db.list_collection_names()
        if collection in collections:
            raise ValueError("Collection " + collection + " exists! This may cause data duplication")
        _db = getattr(self.db, collection)
        return _db
    
    def push_papers(self, papers, collection = "data"):
        """
        pushes papers in format [title, abstract, sitelink, pdflink]
        to db.collection
        """
        
        _db = self._get_collection(collection)
        
        for paper in papers:
            p = {"title": paper[0],
                "abstract": paper[1],
                "sitelink": paper[2],
                "pdflink": paper[3]}
            db.data.insert_one(p)
            
    def push_keywords(self, papers, collection = "keywords"):
        _db = self._get_collection(collection)
        
        tr = TextRank_model(lemmatize = True)
        for paper in papers:
            keywords = tr.predict_tags(paper[1])
            _id = list(db.data.find({'sitelink': paper[2]}))[0]['_id']
            p = {'_id':_id, 'keywords': keywords}
            db.keywords.insert_one(p)