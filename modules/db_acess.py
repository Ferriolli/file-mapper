from typing import Dict
from pymongo import MongoClient
import datetime
import pandas as pd
from loguru import logger


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
        logger.info(f'Inserted {len(data_to_save)} documents into {collection_name} collection')

    def get_data(self, collection_name: str, query: Dict):
        cursor = self._db[collection_name].find(query)
        return pd.DataFrame(list(cursor))

    def get_data_raw(self, collection_name: str, query: Dict, limit: int):
        cursor = self._db[collection_name].find(query).limit(limit)
        return list(cursor)

    def log_information(self, message, status, function_name):
        info_dict = {
            'creation_date': datetime.datetime.now(),
            'function_name': function_name,
            'message': message,
            'status': status
        }

        if status != 'OK':
            self._db['logs'].insert_one(info_dict)

    def collection_exists(self, collection_name: str) -> bool:
        return collection_name in self._db.list_collection_names()


mongo = MongoManager()
