from tools import getArgs
from database_management import database
from constants import USERS_TABLE
from bcrypt import checkpw


def execute(name, password):
    data = database \
        .table(USERS_TABLE) \
        .select('name,password') \
        .eq('name', name) \
        .execute().data
    
    if not data:
        return False

    return checkpw(password.encode(), data[0]['password'].encode())

def endpoint():
    args, isAnyNull = getArgs(
        names=['name', 'password']
    )

    if isAnyNull:
        return
    
    return execute(*args)



