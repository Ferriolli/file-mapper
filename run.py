from extractors.csv_extractor import CSVExtractor
from extractors.xlsx_extractor import ExcelExtractor
from extractors.txt_extrator import TxtExtractor
from modules.custom_exceptions import UnexpectedFileTypeException
from validators.validation_base import Validation
from loguru import logger


class Main:
    """
    Main class, responsible for the execution
    """

    def __init__(self):
        self._file_name = 'data/random-dataset.csv'
        self._extractor = self._get_extractor()
        self._mapper = self._extractor.mapper

    def run(self):
        self._extractor.run()

        if self._mapper['validate']:
            validator = Validation(self._mapper['collection_name'])
            validator.remove_duplicates()

    def _get_extractor(self):
        ext = self._file_name.split('.')[1]
        if ext.lower() == 'csv':
            extractor = CSVExtractor(self._file_name)
        elif ext.lower() == 'xlsx':
            extractor = ExcelExtractor(self._file_name)
        elif ext.lower() == 'txt':
            extractor = TxtExtractor(self._file_name)
        else:
            raise UnexpectedFileTypeException(f'The file type {ext} is not expected')
        logger.success(f'Generated new {str(extractor)}')
        return extractor
