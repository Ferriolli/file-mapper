import json
import yaml
from modules.execution_log import log_info


class FileHandler:
    """
    This class handles file I/O
    """
    def __init__(self):
        pass

    @classmethod
    @log_info
    def read_header(cls, file_path):
        file = FileHandler.open_file(file_path)
        header = file.readlines()[0]
        file.close()
        return header

    @classmethod
    @log_info
    def open_file(cls, file_path):
        return open(file_path, 'r')

    @classmethod
    @log_info
    def read_mapper(cls, file_path):
        file = FileHandler.open_file(file_path)
        if file_path.endswith('.json'):
            file_dict = json.load(file)
        else:
            file_dict = yaml.safe_load(file)
        file.close()
        return file_dict
