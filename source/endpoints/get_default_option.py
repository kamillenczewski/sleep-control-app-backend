from tools import getArgs, log
from database_management import database
from constants import DEFAULT_OPTIONS_TABLE

def execute(name):
    data = database \
        .table(DEFAULT_OPTIONS_TABLE) \
        .select('*') \
        .eq('name', name) \
        .execute().data

    if not data:
        raise ValueError(f'There is no default value for option: {name}')
    
    return data[0]['value']

def endpoint():
    args, isAnyNull = getArgs(
        names=['name'], 
    )
    
    if isAnyNull:
        return

    return execute(*args)


