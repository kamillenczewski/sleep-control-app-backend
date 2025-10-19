from tools import getArgs
from datetime import datetime
from constants import DATETIME_FORMAT
from database_management import database


def datetimesDifference(datetime1: datetime, datetime2: datetime):
    return (datetime1 - datetime2).total_seconds() / 3600

def dateStringToObj(string):
    return datetime.strptime(string, DATETIME_FORMAT)

def createChartData(user_id, valuePrecision=0):
    data = database \
        .table('sleeping') \
        .select('start,end,satisfaction') \
        .eq('user_id', user_id) \
        .execute().data   

    data.sort(key=lambda record: datetime.strptime(record['start'], DATETIME_FORMAT))

    data = [
        {
            'start': dateStringToObj(record['start']),
            'end': dateStringToObj(record['end']),
            'satisfaction': record['satisfaction']
        } 
        for record 
        in data
    ]

    def toChartRecord(record):
        label = record['end'].strftime("%d/%m")
        value = datetimesDifference(record['end'], record['start'])
        value = abs(round(value, valuePrecision))

        return {'label': label, 'value': value, 'extraValue': 0, 'satisfaction': record['satisfaction']}

    return [toChartRecord(record) for record in data]

def labelSortingKey(label):
    day, month = label.split('/')
    day, month = int(day), int(month)

    return month*100 + day

def execute(user_ids, value_precision=0):
    data = [createChartData(userId, value_precision) for userId in user_ids]

    labels = set()
    labelsAndIndexes = dict()
    newData = list()

    for userIndex, userData in enumerate(data):
        for record in userData:
            label = record['label']

            if label in labels:
                labelIndex = labelsAndIndexes[label]
            else:
                labelIndex = len(newData)
                labels.update([label])
                labelsAndIndexes[label] = labelIndex
                newData.append({'label': label, 'other': []})
            
            record = {'userIndex': userIndex, 'value': record['value'], 'extraValue': record['extraValue'], 'satisfaction': record['satisfaction']}

            newData[labelIndex]['other'].append(record)

    return newData

def readIdsString(ids: str):
    stringIds = ids.replace(' ', '').removeprefix('[').removesuffix(']').split(',')

    if not all(stringId.isdigit() for stringId in stringIds):
        return None

    stringIds = [int(stringId) for stringId in stringIds]

    return stringIds


def endpoint():
    args, isAnyNull = getArgs(
        names=['user_ids', 'value_precision'], 
        conversions=[readIdsString, int]
    )

    if isAnyNull:
        return

    return execute(*args)
