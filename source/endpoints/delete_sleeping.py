from tools import getArgs
from database_management import database

def execute(id):
    return (
        database \
            .table('sleeping') 
            .delete() 
            .eq('id', id) 
            .execute().data
    )

def endpoint():
    args, isAnyNull = getArgs(
        names=['id'], 
        conversions=[int]
    )
    
    if isAnyNull:
        return

    return execute(*args)