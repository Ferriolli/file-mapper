from modules.file_handler import FileHandler
from modules.mapper import Mapper
from modules.extractor import Extractor
from modules.db_acess import mongo


class Main:
    """
    Main class, responsible for the execution
    """

    def __init__(self):
        file = 'data/random-dataset.csv'
        header = FileHandler.read_header(file)
        mp = Mapper(header)
        mapper = mp.find_mapper_for_file()
        extractor = Extractor(mapper, file)
        df_save = extractor.create_df()
        mongo.insert_data(df_save, 'finally')


if __name__ == '__main__':
    main_obj = Main()
