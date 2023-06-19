import datetime

from pymongo import MongoClient
import datetime


class MongoManager:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self._db = client['file-mapper']
        self._clear_data_on_insert = True

    def insert_data(self, df, collection_name):
        data_to_save = df.to_dict(orient='records')
        if self._clear_data_on_insert:
            self._db[collection_name].delete_many({})
        self._db[collection_name].insert_many(data_to_save)

    def log_information(self, message, status, function_name):
        info_dict = {
            'creation_date': datetime.datetime.now(),
            'function_name': function_name,
            'message': message,
            'status': status
        }

        if status != 'OK':
            self._db['logs'].insert_one(info_dict)


mongo = MongoManager()
