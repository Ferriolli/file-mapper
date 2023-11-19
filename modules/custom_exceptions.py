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


class UnexpectedFileTypeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class MalformedRegexFindSubException(Exception):
    def __init__(self, message="'regex' must be an instance of list with dicts inside."):
        self.message = message
        super().__init__(self.message)


class ValidationMapperNotFoundException(Exception):
    def __init__(self, message="Validation mapper not found"):
        self.message = message
        super().__init__(self.message)


class MissingKeyInMapperException(Exception):
    def __init__(self, key: str, mapper: str):
        self.message = f"Missing a mandatory key inside validation mapper ({mapper}): {key}"
        super().__init__(self.message)
