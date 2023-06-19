import functools
from modules.db_acess import mongo


def log_info(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            result = function(*args, **kwargs)
            return result
        except Exception as e:
            mongo.log_information('Error', e.__repr__(), function.__name__)
            raise e
    return wrapper
