from tools import getArgs
from database_management import database
from constants import USER_OPTIONS_TABLE

def execute(user_id, name, value):
    return database \
        .table(USER_OPTIONS_TABLE) \
        .insert({'user_id': user_id, 'name': name, 'value': value}) \
        .execute().data[0]

def endpoint():
    args, isAnyNull = getArgs(
        names=['user_id', 'name', 'value'], 
        conversions=[int, None, None]
    )
    
    if isAnyNull:
        return

    return execute(*args)


