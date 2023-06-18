from pymongo import MongoClient
from modules.custom_exceptions import CollectionNotSetException


class MongoManager:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self._db = client['file-mapper']

    def insert_data(self, df, collection):
        data_to_save = df.to_dict(orient='records')
        self._db[collection].insert_many(data_to_save)


mongo = MongoManager()
