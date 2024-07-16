from pymongo import MongoClient
from config.settings import MONGO_URI, MONGO_DB_NAME

class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]

    def get_collection(self, collection_name):
        return self.db[collection_name]

# Singleton pattern for MongoDB client
mongodb_client = MongoDBClient()
