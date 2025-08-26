from tools import getArgs
from database_management import database
from constants import USER_OPTIONS_TABLE
from endpoints.get_default_option import execute as getDefaultOption
from endpoints.add_user_option import execute as addUserOption

def execute(user_id, name):
    data = database \
        .table(USER_OPTIONS_TABLE) \
        .select('*') \
        .eq('user_id', user_id) \
        .eq('name', name) \
        .execute().data

    if not data:
        value = getDefaultOption(name)
        addUserOption(user_id, name, value)
        return value
    
    return data[0]['value']

def endpoint():
    args, isAnyNull = getArgs(
        names=['user_id', 'name'], 
        conversions=[int, None]
    )
    
    if isAnyNull:
        return

    return execute(*args)


