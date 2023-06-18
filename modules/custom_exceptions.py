class MultipleMappersFoundException(Exception):
    def __init__(self, message='More than one mapper found for the same file'):
        self.message = message
        super().__init__(self.message)


class MapperNotFoundException(Exception):
    # TODO: Add file_name in Exception message
    def __init__(self, message='Mapper not found for file'):
        self.message = message
        super().__init__(self.message)


class CollectionNotSetException(Exception):
    def __init__(self, message="'collection' property must be set before trying to access the db"):
        self.message = message
        super().__init__(self.message)
