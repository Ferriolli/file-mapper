from typing import Dict
from datetime import datetime
import pandas as pd
from loguru import logger
from modules.execution_log import log_info


class Extractor:
    def __init__(self, mapper: Dict, file_name):
        self._mapper = mapper
        self.file_name = file_name
        self._full_df = pd.read_csv(file_name, sep=self._mapper['separator'])
        self._extracted_df = pd.DataFrame()

    @log_info
    def create_df(self):
        for index, info in self._mapper['columns'].items():
            self._extracted_df[info['name']] = self._full_df.iloc[:, int(index)]
            if 'regex' in info:
                for regex in info['regex']:
                    logger.info(f"Replacing: {regex['find']} for {regex['sub']} on column {info['name']}")
                    self.replace_content(info['name'], regex)
        self.add_system_columns()
        self.change_dtypes()
        return self._extracted_df

    @log_info
    def add_system_columns(self):
        self._extracted_df['creation_date'] = datetime.now()

    @log_info
    def change_dtypes(self):
        dtypes = {
            'string': str,
            'int': 'int32',
            'float': float
        }

        for index, info in self._mapper['columns'].items():
            self._extracted_df[info['name']] = self._extracted_df[info['name']].astype(dtypes[info['type']])

    @log_info
    def replace_content(self, column: str, replacement: Dict):
        self._extracted_df[column] = self._extracted_df[column].str.replace(fr'{replacement["find"]}',
                                                                            replacement['sub'],
                                                                            regex=True)
