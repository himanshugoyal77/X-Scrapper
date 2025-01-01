from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv() 

class ConnectDB:
    def __init__(self):
        self.client = MongoClient(
            os.getenv('MONGO_URI')
        )
        self.db = self.client['stir'] 
        self.collection = self.db['myCollection']  
        
    def connect(self):
        return self.client

    def insert(self, data):
        self.collection.insert_one(data)
        
    def find(self, query):
        return self.collection.find(query)
    
    def find_one(self, query):
        return self.collection.find_one(query)
    
    def update(self, query, data):
        self.collection.update_one(query, data)
        
    def delete(self, query):
        self.collection.delete_one(query)
        
    def delete_many(self, query):
        self.collection.delete_many(query)
        
    def drop(self):
        self.collection.drop()
        
    def count(self):
        self.collection.count()