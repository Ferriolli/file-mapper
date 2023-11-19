from extractors.extractor_base import ExtractorBase
from modules.db_acess import mongo
from modules.file_handler import FileHandler
import pandas as pd


class TxtExtractor(ExtractorBase):
    def __init__(self, file_name: str):
        super().__init__(file_name)

    def __str__(self):
        return 'txt file extractor'

    def get_header(self):
        file = FileHandler.open_file(self._file_name)
        header = file.readlines()[0]
        file.close()
        return header

    def create_df(self):
        file = FileHandler.open_file(self._file_name)
        data = []
        for row in file.readlines():
            cur_row = {}
            for index, info in self.mapper['columns'].items():
                start = int(index.split('-')[0])
                end = int(index.split('-')[1])
                cur_row.update({info['name']: row[start:end].replace('\n', '')})
            data.append(cur_row)
        self._extracted_df = pd.DataFrame(data)
        self.add_system_columns()
        self.replace_content(self.mapper)
        self.change_dtypes(self.mapper)
        file.close()

    def run(self):
        self.create_df()
        mongo.insert_data(self._extracted_df, self.mapper['collection_name'])
