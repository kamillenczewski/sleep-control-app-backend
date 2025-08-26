from database_management import database
from constants import USERS_TABLE

def execute():
    data = database \
        .table(USERS_TABLE) \
        .select('id,name') \
        .execute().data

    return data

def endpoint():
    return execute()

