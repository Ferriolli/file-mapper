from loguru import logger
import pandas as pd
from modules.db_acess import mongo
from modules.file_handler import FileHandler
from modules.custom_exceptions import MissingKeyInMapperException


class Validation:
    # Todo: Define a way to choose which validations are gonna be made, via the json configuration file
    # Idea: Create a class (or function) that goes through every validation necessary, before saving into the DB
    def __init__(self, collection_name: str):
        self._collection_name: str = collection_name
        self._full_df: pd.DataFrame = mongo.get_data(collection_name=self._collection_name, query={})
        self._config = FileHandler.read_mapper(f'validation_mappers/{self._collection_name}')
        self.validate_mapper()

    def remove_duplicates(self):
        if len(self._config['duplicate_keys']) == 0:
            return
        dup = self._full_df.duplicated(subset=self._config['duplicate_keys'], keep=self._config['keep'])
        invalid_data = self._full_df[dup]
        valid_data = self._full_df.drop_duplicates(subset=self._config['duplicate_keys'], keep=self._config['keep'])

        del self._full_df

        self.save_data(valid_data, invalid_data)

    def save_data(self, valid_data: pd.DataFrame, invalid_data: pd.DataFrame = None):
        valid_collection_name = f'{self._collection_name}_valid'
        invalid_collection_name = f'{self._collection_name}_invalid'

        if len(invalid_data) <= 0:
            logger.warning(f'No invalid data was generated')
        else:
            mongo.insert_data(df=invalid_data, collection_name=invalid_collection_name)

        if len(valid_data) <= 0:
            logger.warning(f'No valid data was generated')
        else:
            mongo.insert_data(df=valid_data, collection_name=valid_collection_name)

    def validate_mapper(self):
        main_keys = ['duplicate_keys', 'keep', 'schema']
        for key in main_keys:
            if key not in self._config:
                logger.error(f'Missing mandatory key in validation mapper ({self._collection_name}): {key}')
                raise MissingKeyInMapperException(key, self._collection_name)
