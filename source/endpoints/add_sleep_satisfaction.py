from tools import getArgs
from database_management import database
from constants import SLEEP_SATISFACTION_TABLE

def execute(dateId, percent):
    if not 0 <= percent <= 100:
        raise ValueError('Percent should be a float number in interval [0, 100]!')

    return database \
        .table(SLEEP_SATISFACTION_TABLE) \
        .insert({'date_id': dateId, 'percent': percent}) \
        .execute().data[0]

def endpoint():
    args, isAnyNull = getArgs(
        names=['dateId', 'percent'], 
        defaults=None,
        conversions=[int, float]
    )
    
    if isAnyNull:
        return

    return execute(*args)