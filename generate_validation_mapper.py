import sys
import json
import yaml
from modules.db_acess import mongo


def generate_validation_mapper(collection_name: str, mode: str):
    base_dict = {
        'duplicate_keys': [],
        'keep': False,
        'schema': {

        }
    }

    if mongo.collection_exists(collection_name):
        system_cols = ['_id', 'creation_date']
        ex = mongo.get_data_raw(collection_name, {}, 1)
        ex = ex[0]
        for key, value in ex.items():
            if key not in system_cols:
                base_dict['schema'].update({key: []})

    with open(f'validation_mappers/{collection_name}.{mode}', 'w') as e:
        if mode == 'json':
            json.dump(base_dict, e, indent=4)
        if mode == 'yaml':
            yaml.dump(base_dict, e)


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print(f'Usage: python3 generate_validation_mapper.py <collection_name> <mode>\n'
              f'Where collection name is the name of the collection in MongoDb to generate the mapper file\n'
              f'And mode can be "json" or "yaml", defining the format to save the file')
        sys.exit('Error: Aborting due to missing parameters...')

    _collection_name = sys.argv[1]
    _mode = sys.argv[2]

    if _mode not in ['json', 'yaml']:
        print(f'The second parameter must be either "json" or "yaml", to indicate the format to save the file.')
        sys.exit(f'Error: Aborting due to invalid parameters...')

    generate_validation_mapper(collection_name=_collection_name, mode=_mode)
