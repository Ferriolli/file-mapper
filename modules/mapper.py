import os
import re
from modules.file_handler import FileHandler
from modules.custom_exceptions import MultipleMappersFoundException, MapperNotFoundException
from loguru import logger


class Mapper:
    """
    This class is responsible for find the correct mapper for the file
    """
    def __init__(self, file_header):
        self._file_header = file_header

    def find_mapper_for_file(self):
        identified = []
        for file in os.listdir('mappers/'):
            mapper = FileHandler.read_json(f'mappers/{file}')
            identifier = mapper['identifier']
            if re.match(fr'{identifier}', self._file_header):
                identified.append(file)

        if len(identified) > 1:
            raise MultipleMappersFoundException

        if len(identified) == 0:
            raise MapperNotFoundException

        logger.success(f'Found mapper.')
        return FileHandler.read_json(f'mappers/{identified[0]}')
