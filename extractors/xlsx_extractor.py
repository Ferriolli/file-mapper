import pandas as pd
from extractors.extractor_base import ExtractorBase
from modules.db_acess import mongo


class ExcelExtractor(ExtractorBase):
    def __init__(self, file_name: str):
        super().__init__(file_name)
        self._full_df = pd.read_excel(file_name)

    def __str__(self):
        return 'xlsx file extractor'

    def get_header(self):
        df = pd.read_excel(self._file_name, nrows=5)
        return df.to_csv(sep=',', index_label=False).split('\n')[0]

    def run(self):
        self.create_df()
        mongo.insert_data(self._extracted_df, self.mapper['collection_name'])
