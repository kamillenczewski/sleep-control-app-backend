from tools import getArgs
from database_management import database
from constants import DATES_TABLE

def execute(userId, data, type):
    return database \
        .table(DATES_TABLE) \
        .insert({'user_id': userId, 'datetime': data, 'type': type}) \
        .execute().data[0]  

def endpoint():
    args, isAnyNull = getArgs(
        names=['userId', 'datetime', 'type'], 
        defaults=None,
        conversions=[int, None, None]
    )
    
    if isAnyNull:
        return

    return execute(*args)