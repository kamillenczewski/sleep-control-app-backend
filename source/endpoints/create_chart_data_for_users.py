from endpoints.create_chart_data import execute as createChartData
from tools import getArgs

def labelSortingKey(label):
    day, month = label.split('/')
    day, month = int(day), int(month)

    return month*100 + day

def execute(userIds, unit, valuePrecision):
    data = [createChartData(userId, unit, valuePrecision) for userId in userIds]

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
            
            newData[labelIndex]['other'].append({'userIndex': userIndex, 'value': record['value'], 'extraValue': record['extraValue'], 'satisfactionPercent': record['satisfactionPercent']})

    return newData

def readIdsString(ids: str):
    stringIds = ids.replace(' ', '').removeprefix('[').removesuffix(']').split(',')

    if not all(stringId.isdigit() for stringId in stringIds):
        return None

    stringIds = [int(stringId) for stringId in stringIds]

    return stringIds


def endpoint():
    args, isAnyNull = getArgs(
        names=['userIds', 'unit', 'valuePrecision'], 
        conversions=[readIdsString, None, int]
    )

    if isAnyNull:
        return

    return execute(*args)
