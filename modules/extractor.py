from typing import Dict
from datetime import datetime
import pandas as pd


class Extractor:
    def __init__(self, mapper: Dict, file_name):
        self._mapper = mapper
        self.file_name = file_name
        self._full_df = pd.read_csv(file_name, sep=self._mapper['separator'])
        self._extracted_df = pd.DataFrame()

    def create_df(self):
        for index, info in self._mapper['columns'].items():
            self._extracted_df[info['name']] = self._full_df.iloc[:, int(index)]
        self.add_system_columns()
        return self._extracted_df

    def add_system_columns(self):
        self._extracted_df['creation_date'] = datetime.now()
