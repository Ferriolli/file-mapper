import json
import yaml
from modules.execution_log import log_info
from modules.custom_exceptions import MultipleMappersFoundException, MapperNotFoundException
import os
import re
from loguru import logger
from typing import Dict


class FileHandler:
    """
    This class handles file management
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
    def read_mapper(cls, file_path: str) -> Dict:
        """
        This functions reads a mapper file, basically a json containing the necessary information to
        extract or validate a file.
        @param file_path: The path leading to a file, may or may not contain .json or .yaml in the end eg:
            a file is named config_file.json
            if this param is passed as config_file, this function handles the extension.
        @return: Python dictionary of the yaml or json file
        """
        if '.' not in file_path:
            try:
                file = FileHandler.open_file(file_path + '.yaml')
            except FileNotFoundError:
                file = FileHandler.open_file(file_path + '.json')
        else:
            file = FileHandler.open_file(file_path)
        if file_path.endswith('.json'):
            file_dict = json.load(file)
        else:
            file_dict = yaml.safe_load(file)
        file.close()
        return file_dict

    @classmethod
    @log_info
    def find_mapper_for_file(cls, header):
        identified = []
        for file in os.listdir('mappers/'):
            mapper = FileHandler.read_mapper(f'mappers/{file}')
            identifier = mapper['identifier']
            if re.match(fr'{identifier}', header):
                identified.append(file)

        if len(identified) > 1:
            raise MultipleMappersFoundException

        if len(identified) == 0:
            raise MapperNotFoundException

        logger.success(f'Found mapper.')
        return FileHandler.read_mapper(f'mappers/{identified[0]}')
