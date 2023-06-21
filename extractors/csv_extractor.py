import pandas as pd
from extractors.extractor_base import ExtractorBase
from loguru import logger
from modules.file_handler import FileHandler
from modules.db_acess import mongo


class CSVExtractor(ExtractorBase):
    def __init__(self, file_name: str):
        super().__init__(file_name)
        self._full_df = self.load_df(self._mapper)

    def get_header(self):
        file = FileHandler().open_file(self._file_name)
        header = file.readlines()[0]
        file.close()
        return header

    def load_df(self, mapper):
        return pd.read_csv(self._file_name, sep=mapper['separator'])

    def run(self):
        self.create_df()
        mongo.insert_data(self._extracted_df, self._mapper['collection_name'])
