import pymongo, heapq

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
        
    def search_text(self, text, num_results = 10):
        pass
        