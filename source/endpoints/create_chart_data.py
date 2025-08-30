from tools import getArgs
from datetime import datetime
from constants import DATETIME_FORMAT, DATES_TABLE
from database_management import database
from extended_list import List



def getDatetimesFromId(user_id, type):
    data = database \
        .table(DATES_TABLE) \
        .select('user_id,type,datetime') \
        .eq('user_id', user_id) \
        .eq('type', type) \
        .execute().data   

    dates = List(data).map("record => record['datetime']")
    dates.sort(key=lambda date: datetime.strptime(date, DATETIME_FORMAT))

    return dates


def datetimesDifference(datetime1: datetime, datetime2: datetime, unit):
    """
    outputFormat: H - hours, M - minutes, S - seconds
    """

    divisionFactor = 60 * 60 if unit == 'H' else 60 if unit == 'M' else 'S'

    return (datetime1 - datetime2).total_seconds() / divisionFactor


def dateStringToObj(string):
    return datetime.strptime(string, DATETIME_FORMAT)


def createSleepAmountData(wakeupDates, sleeptimeDates, unit='H', valuePrecision=0):
    if len(wakeupDates) == 0 or len(sleeptimeDates) == 0:
        return []

    wakeupObjects = [dateStringToObj(string) for string in wakeupDates]
    sleeptimeObjects = [dateStringToObj(string) for string in sleeptimeDates]

    def indexToLabelAndValue(index):
        label = sleeptimeObjects[index].strftime("%d/%m")
        value = datetimesDifference(wakeupObjects[index], sleeptimeObjects[index], unit)
        value = abs(round(value, valuePrecision))

        return {'label': label, 'value': value, 'extraValue': 0, 'satisfactionPercent': 30}

    data = [indexToLabelAndValue(index) for index in range(min(len(wakeupDates), len(sleeptimeDates)))]

    return data


def execute(user_id, unit, value_precision):
    wakeupDates = getDatetimesFromId(user_id, 'wakeup')
    sleeptimeDates = getDatetimesFromId(user_id, 'sleeptime')
    chartData = createSleepAmountData(wakeupDates, sleeptimeDates, unit, value_precision)
    return chartData

def endpoint():
    args, isAnyNull = getArgs(
        names=['user_id', 'unit', 'value_precision'], 
        conversions=[int, None, int]
    )

    if isAnyNull:
        return

    return execute(*args)