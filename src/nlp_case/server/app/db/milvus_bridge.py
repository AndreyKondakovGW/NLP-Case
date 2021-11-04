import csv
import pandas as pd
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection

class MilvusBridge:
    def __init__(self):
        self.connection = connections.connect(host='localhost', port='19530')
        self.collection = None
        
    def push_embeddings(self, file):
        df = pd.read_csv(file, sep=',')
        
        cols = list(df.columns.values)
        cols.pop(cols.index('_id'))
        cols.pop(cols.index('Unnamed: 0'))
        
        dim = len(cols)
        #milvus does not support strings, LOL
        #so we need to squeeze _id into INT64s
        data = df[['_id']]
        data['id_timestamp'] = data['_id'].apply(lambda x: int(x[:8], 16))
        data['id_proc'] = data['_id'].apply(lambda x: int(x[8:18], 16))
        data['_id'] = data['_id'].apply(lambda x: int(x[18:24], 16))
        
        data['features'] = df[cols].astype('float32').values.tolist()
        
        default_fields = [
                        FieldSchema(name='_id', dtype=DataType.INT64, is_primary=True),
                        FieldSchema(name='id_timestamp', dtype=DataType.INT64),
                        FieldSchema(name='id_proc', dtype=DataType.INT64),
                        FieldSchema(name='features', dtype=DataType.FLOAT_VECTOR, dim = dim)
                    ]
        if 'similarity_features' in self.connection.list_collections():
            self.connection.drop_collection(collection_name='similarity_features')
                    
        schema = CollectionSchema(fields=default_fields)
        self.collection = Collection(name='similarity_features', schema=schema)
        
        collection.insert(data)
        
        #inner product (IP) is equivalent to cosine sim on normalized data
        index = {"index_type": "IVF_FLAT", "params": {"nlist": 128}, "metric_type": "IP"}
        collection.create_index(field_name="features", index_params=index)
        collection.load()
        
    def find_similar(self, features, num_results = 10):
        if self.collection is None:
            if not 'similarity_features' in self.connection.list_collections():
                raise Error("milvus database is not populated, but you're trying to access it!")
            self.collection = Collection(name='similarity_features')
    
        search_params = {"metric_type": "IP", "params": {"nprobe": 10}}
        
        results = []
        search_res = self.collection.search(
            [list(features)], "features", param=search_params, limit = num_results,
            output_fields=["_id", "id_timestamp", "id_proc"]
        )
        
        for raw_res in search_res:
            for result in raw_res:
                entity = result.entity
                _id = entity._id
                id_timestamp = entity.id_timestamp
                id_proc = entity.id_proc
                
                _id = (hex(id_timestamp).lstrip("0x") +
                       hex(id_proc).lstrip("0x") + 
                       hex(_id).lstrip("0x"))
                       
                results.append(_id)
                
        return results
