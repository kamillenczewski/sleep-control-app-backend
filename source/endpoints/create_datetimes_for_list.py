from tools import getArgs
from datetime import datetime
from constants import DATETIME_FORMAT, DATES_TABLE
from database_management import database
from extended_list import List

def getDatetimesAndIdsFromUserId(userId, type):
    data = database \
        .table(DATES_TABLE) \
        .select('id,user_id,type,datetime') \
        .eq('user_id', userId) \
        .eq('type', type) \
        .execute().data   
    
    dates = List(data).map("record => {'datetime': record['datetime'], 'id': record['id']}")
    dates.sort(key=lambda date: datetime.strptime(date['datetime'], DATETIME_FORMAT))

    return dates

def execute(userId, type):
    def convert(record):
        return {
            'id': record['id'],
            'datetime': datetime.strptime(record['datetime'], DATETIME_FORMAT).strftime('%d/%m/%Y %H'),
        }

    return [convert(record) for record in getDatetimesAndIdsFromUserId(userId, type)]

def endpoint():
    args, isAnyNull = getArgs(
        names=['userId', 'type'], 
        defaults=None,
        conversions=[int, None]
    )
    
    if isAnyNull:
        return

    return execute(*args)
