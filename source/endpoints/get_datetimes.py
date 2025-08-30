from tools import getArgs
from database_management import database
from constants import DATES_TABLE, DATETIME_FORMAT
from extended_list import List
from datetime import datetime

def execute(id, type):
    data = database \
        .table(DATES_TABLE) \
        .select('user_id,type,datetime') \
        .eq('user_id', id) \
        .eq('type', type) \
        .execute().data   
    
    dates = List(data).map("record => record['datetime']")
    dates.sort(key=lambda date: datetime.strptime(date, DATETIME_FORMAT))

    return dates

def endpoint():
    args, isAnyNull = getArgs(
        names=['id', 'type'], 
        conversions=[int, None]
    )
    
    if isAnyNull:
        return

    return execute(*args)