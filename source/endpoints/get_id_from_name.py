from tools import getArgs
from database_management import database
from constants import USERS_TABLE
from extended_list import List

def execute(name):
    data = database \
        .table(USERS_TABLE) \
        .select('id,name') \
        .eq('name', name) \
        .execute().data   
    
    return List(data).first()['id']

def endpoint():
    args, isAnyNull = getArgs(
        names=['name'],
    )
    
    if isAnyNull:
        return

    return execute(*args)