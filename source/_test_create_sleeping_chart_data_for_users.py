from endpoints.create_sleeping_chart_data import execute as createChartData
from tools import getArgs

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

print(execute([16,18]))