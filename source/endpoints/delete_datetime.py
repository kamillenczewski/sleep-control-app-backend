from tools import getArgs
from database_management import database
from constants import DATES_TABLE

def execute(id):
    return database \
        .table(DATES_TABLE) \
        .delete() \
        .eq('id', id) \
        .execute().data

def endpoint():
    args, isAnyNull = getArgs(
        names=['id'], 
        conversions=[int]
    )
    
    if isAnyNull:
        return

    return execute(*args)