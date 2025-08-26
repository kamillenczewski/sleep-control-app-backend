from tools import getArgs, writeFile
from database_management import database
from constants import USERS_TABLE

def execute(name):
    records = database \
        .table(USERS_TABLE) \
        .select('name') \
        .execute().data
    
    return name in [record['name'] for record in records]

def endpoint():
    args, isAnyNull = getArgs(
        names=['name'], 
        defaults=None,
        conversions=None
    )

    if isAnyNull:
        return

    return execute(*args)