from google_sheets_api import get
from tools import transpose

USERS_RANGE = 'Ogólnie!2:2'
DATETIMES_RANGE = 'Ogólnie!C4:L'

def getUsers():
    return [name.strip() for name in get(USERS_RANGE)[0] if name.strip() != '']

def countBeginEmptyStrings(array):
    counter = 0

    for item in array:
        if item.strip() != '':
            break

        counter += 1

    return counter

# def normalizeDates(dates): 
#     return [date.ljust('') for date in dates]

def exportDates():
    table = get(DATETIMES_RANGE)
    users = getUsers()
    maxLength = len(max(*table, key=len))

    for subArray in table:
        if len(subArray) < maxLength:
            subArray.extend([''] * (maxLength - len(subArray)))

    table = transpose(table)

    wakeUpColumns = table[::2]
    sleepColumns = table[1::2]

    for user, wakeupDatesList, sleepDatesList in zip(users, wakeUpColumns, sleepColumns):
        if countBeginEmptyStrings(wakeupDatesList) == countBeginEmptyStrings(sleepDatesList):
            wakeupDatesList.pop(0)

    wakeUpColumns = [[item for item in column if item.strip() != ''] for column in wakeUpColumns]
    sleepColumns = [[item for item in column if item.strip() != ''] for column in sleepColumns]

    array = []

    for user, wakeupDatesList, sleepDatesList in zip(users, wakeUpColumns, sleepColumns):
        if len(wakeupDatesList) > len(sleepDatesList):
            wakeupDatesList.pop(0)
        elif len(sleepDatesList) > len(wakeupDatesList):
            sleepDatesList.pop()

        array.append({'user': user, 'wakeup': wakeupDatesList, 'sleeptime': sleepDatesList})

    return array


if __name__ == '__main__':
    from tools import writeFile
    from json import dumps

    writeFile('export_output.json', dumps(dict(array=exportDates()), ensure_ascii=False))