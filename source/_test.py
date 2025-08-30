from database_management import database
from endpoints.get_all_options import execute as getAllOptions
from tools import getArgs

def execute(user_id):
    defaultOptions = getAllOptions()

    actualOptions = (
        database
            .table('users_and_options')
            .select('*')
            .eq('user_id', user_id)
            .execute().data
    )
    actualOptions = {
        record['option_id']: record
        for record 
        in actualOptions
    }

    data = [
        {
            **record, 
            'value': actualOptions[record['option_id']]['value'] if record['option_id'] in actualOptions else None
        } 
        for record 
        in defaultOptions
    ]

    return data

def endpoint():
    args, isAnyNull = getArgs(
        names=['user_id'], 
        conversions=[int]
    )
    
    if isAnyNull:
        return

    return execute(*args)


print(execute(16))