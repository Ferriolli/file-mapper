from modules.file_handler import FileHandler
from modules.mapper import Mapper
from modules.extractor import Extractor
from modules.db_acess import mongo


class Main:
    """
    Main class, responsible for the execution
    """

    def __init__(self):
        self._file_name = 'data/random-dataset.csv'

    def run(self):
        header = FileHandler.read_header(self._file_name)
        mp = Mapper(header)
        mapper = mp.find_mapper_for_file()
        extractor = Extractor(mapper, self._file_name)
        df_save = extractor.create_df()
        mongo.insert_data(df_save, mapper['collection_name'])


if __name__ == '__main__':
    main_obj = Main()
    main_obj.run()
