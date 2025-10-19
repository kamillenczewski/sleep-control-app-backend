from tools import getArgs
from database_management import database

def execute(user_id):
    return (
        database \
            .table('sleeping') 
            .select('*') 
            .eq('user_id', user_id) 
            .execute().data
    )

def endpoint():
    args, isAnyNull = getArgs(
        names=['user_id'], 
        conversions=[int]
    )
    
    if isAnyNull:
        return

    return execute(*args)