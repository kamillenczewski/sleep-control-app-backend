from tools import getArgs
from datetime import datetime
from constants import DATETIME_FORMAT, DATES_TABLE
from database_management import database

def getDatetime(id):
    return database \
        .table(DATES_TABLE) \
        .select('id,datetime') \
        .eq('id', id) \
        .execute().data[0]['datetime']

def execute(id):
    return {
        'id': id,
        'datetime': datetime.strptime(getDatetime(id), DATETIME_FORMAT).strftime('%d/%m/%Y %H'),
    }

def endpoint():
    args, isAnyNull = getArgs(
        names=['id']
    )
    
    if isAnyNull:
        return

    return execute(*args)