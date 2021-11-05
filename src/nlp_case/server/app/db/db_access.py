import pymongo, heapq
from bson.objectid import ObjectId

class DBAccess:
    
    def __init__(self, pwd):
        self.client = pymongo.MongoClient("mongodb+srv://nlp-access:"+pwd+"@cluster0.oelvn.mongodb.net/Cluster0?retryWrites=true&w=majority")
        self.db = self.client.nlp
        self.db_kw = self.db.keywords
        self.db_data = self.db.data
        
    def search_keywords(self, keywords, num_results = 10):
        query = {"keywords": { "$in": keywords}}
        cursor = self.db_kw.find(query)
        result = list(cursor)

        ids = {}
        for r in result:
            ids[r['_id']] = sum(el in keywords for el in r['keywords'])
            
        largest = heapq.nlargest(num_results, ids, key=ids.get)
            
        papers = self.db_data.find({"_id": {"$in": largest}})
        papers_list = [] 
        for p in papers: #this is where the application design fails. TODO: ???
            papers_list.append([p['title'], p['abstract'], p['sitelink'], p['pdflink']])
            
        return papers_list
        
    #[!!!] does not reset itself automatically.
    #needs .rewind() to iterate over DB again
    def get_papers_iterator(self):
        return self.db_data.find()
        
    def get_all_keywords(self):
        return self.db_kw.distinct("keywords")
        
    def get_paper_by_id(self, id):
        cursor = self.db_data.find({"_id": ObjectId(id)})
        if cursor.count() == 0:
            raise ValueError("No paper with this ID found!")

        return cursor[0]
        
    def search_text(self, text, num_results = 10):
        pass

        