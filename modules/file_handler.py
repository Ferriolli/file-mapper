import json


class FileHandler:
    """
    This class handles file I/O
    """
    def __init__(self):
        pass

    @classmethod
    def read_header(cls, file_path):
        file = FileHandler.open_file(file_path)
        return file.readlines()[0]

    @classmethod
    def open_file(cls, file_path):
        return open(file_path, 'r')

    @classmethod
    def read_json(cls, file_path):
        return json.load(FileHandler.open_file(file_path))
