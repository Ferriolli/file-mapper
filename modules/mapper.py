import os
import re
from modules.file_handler import FileHandler
from modules.custom_exceptions import MultipleMappersFoundException, MapperNotFoundException
from modules.execution_log import log_info
from loguru import logger


class Mapper:
    """
    This class is responsible for finding the correct mapper for the file
    """
    def __init__(self, file_header):
        self._file_header = file_header

    @log_info
    def find_mapper_for_file(self):
        identified = []
        for file in os.listdir('mappers/'):
            mapper = FileHandler.read_mapper(f'mappers/{file}')
            identifier = mapper['identifier']
            if re.match(fr'{identifier}', self._file_header):
                identified.append(file)

        if len(identified) > 1:
            raise MultipleMappersFoundException

        if len(identified) == 0:
            raise MapperNotFoundException

        logger.success(f'Found mapper.')
        return FileHandler.read_mapper(f'mappers/{identified[0]}')
