from abc import ABC, abstractmethod
from modules.execution_log import log_info
from modules.file_handler import FileHandler
from modules.custom_exceptions import MalformedRegexFindSubException
from datetime import datetime
from typing import Dict
import pandas as pd
from loguru import logger


class ExtractorBase(ABC):
    def __init__(self, file_name: str):
        self._extracted_df = pd.DataFrame()
        self._file_name = file_name
        self.mapper = FileHandler.find_mapper_for_file(self.get_header())

    @log_info
    def create_df(self):
        for index, info in self.mapper['columns'].items():
            self._extracted_df[info['name']] = self._full_df.iloc[:, int(index)]
        self.add_system_columns()
        self.replace_content(self.mapper)
        self.change_dtypes(self.mapper)

    @abstractmethod
    def get_header(self):
        pass

    @log_info
    def add_system_columns(self):
        self._extracted_df['creation_date'] = datetime.now()

    @log_info
    def change_dtypes(self, mapper: Dict):
        dtypes = {
            'string': str,
            'int': 'int32',
            'float': float
        }

        for index, info in mapper['columns'].items():
            self._extracted_df[info['name']] = self._extracted_df[info['name']].astype(dtypes[info['type']])

    @log_info
    def replace_content(self, mapper: Dict):
        for index, info in mapper['columns'].items():
            if 'regex' in info:
                if not isinstance(info['regex'], list):
                    raise MalformedRegexFindSubException
                for regex in info['regex']:
                    logger.info(f"Replacing: {regex['find']} for {regex['sub']} on column {info['name']}")
                    self._extracted_df[info['name']] = self._extracted_df[info['name']].str.replace(fr'{regex["find"]}',
                                                                                                    regex['sub'],
                                                                                                    regex=True)
