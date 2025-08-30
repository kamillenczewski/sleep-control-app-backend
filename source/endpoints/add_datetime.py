from tools import getArgs
from database_management import database
from constants import DATES_TABLE

def execute(user_id, data, type):
    return database \
        .table(DATES_TABLE) \
        .insert({'user_id': user_id, 'datetime': data, 'type': type}) \
        .execute().data[0]  

def endpoint():
    args, isAnyNull = getArgs(
        names=['user_id', 'datetime', 'type'], 
        conversions=[int, None, None]
    )
    
    if isAnyNull:
        return

    return execute(*args)