from tools import getArgs
from database_management import database
from constants import SLEEP_SATISFACTION_TABLE

def execute(date_id, percent):
    if not 0 <= percent <= 100:
        raise ValueError('Percent should be a float number in interval [0, 100]!')

    return database \
        .table(SLEEP_SATISFACTION_TABLE) \
        .insert({'date_id': date_id, 'percent': percent}) \
        .execute().data[0]

def endpoint():
    args, isAnyNull = getArgs(
        names=['date_id', 'percent'], 
        conversions=[int, float]
    )
    
    if isAnyNull:
        return

    return execute(*args)