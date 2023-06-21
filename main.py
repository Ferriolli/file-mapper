from extractors.csv_extractor import CSVExtractor
from extractors.xlsx_extractor import ExcelExtractor
from modules.custom_exceptions import UnexpectedFileTypeException


class Main:
    """
    Main class, responsible for the execution
    """

    def __init__(self):
        self._file_name = 'data/MOCK_DATA.xlsx'

    def run(self):
        extractor = self._get_extractor()
        extractor.run()

    def _get_extractor(self):
        ext = self._file_name.split('.')[1]

        if ext.lower() == 'csv':
            extractor = CSVExtractor(self._file_name)
        elif ext.lower() == 'xlsx':
            extractor = ExcelExtractor(self._file_name)
        else:
            raise UnexpectedFileTypeException(f'The file type {ext} is not expected')
        return extractor


if __name__ == '__main__':
    main_obj = Main()
    main_obj.run()
