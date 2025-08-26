from tools import getArgs
from database_management import database
from constants import USER_OPTIONS_TABLE

def execute(user_id):
    data = database \
        .table(USER_OPTIONS_TABLE) \
        .select('name,value') \
        .eq('user_id', user_id) \
        .execute().data

    data = {record['key']: record['value'] for record in data}

    return data

def endpoint():
    args, isAnyNull = getArgs(
        names=['user_id'], 
        conversions=[int]
    )
    
    if isAnyNull:
        return

    return execute(*args)
print(execute(18))