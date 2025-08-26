from tools import getArgs
from database_management import database
from constants import USERS_TABLE
from bcrypt import hashpw, gensalt


def execute(name, password):
    return database \
        .table(USERS_TABLE) \
        .insert({'name': name, 'password': hashpw(password.encode(), gensalt()).decode()}) \
        .execute().data[0]

def endpoint():
    args, isAnyNull = getArgs(
        names=['name', 'password'], 
        defaults=None,
        conversions=None
    )
    
    if isAnyNull:
        return

    return execute(*args)