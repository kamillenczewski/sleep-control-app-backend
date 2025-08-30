from database_management import database
from json import loads

# get default options
def execute():
    data = database \
        .table('options') \
        .select("*") \
        .execute().data

    data = [
        {
            'default_value': record['default_value'],
            'value': None,
            'option_id': record['id'],
            'name': record['name'],
            'other': loads(record['other']) if record['other'] else None,
            'type': record['type']
        }
        for record 
        in data
    ]

    return data

def endpoint():
    return execute()