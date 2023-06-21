from extractors.csv_extractor import CSVExtractor
from extractors.xlsx_extractor import ExcelExtractor
from extractors.txt_extrator import TxtExtractor
from modules.custom_exceptions import UnexpectedFileTypeException
from loguru import logger


class Main:
    """
    Main class, responsible for the execution
    """

    def __init__(self):
        self._file_name = 'data/random-dataset.csv'

    def run(self):
        extractor = self._get_extractor()
        extractor.run()

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


if __name__ == '__main__':
    main_obj = Main()
    main_obj.run()
