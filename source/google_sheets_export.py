from google_sheets_api import get
from tools import returnList

SHEET_NAME = 'Main'
USERS_RANGE = f'{SHEET_NAME}!1:1'
DATETIMES_RANGE = f'{SHEET_NAME}!A3:J'

def getUsers():
    return [name.strip() for name in get(USERS_RANGE)[0] if name.strip() != '']


def transpose(table):
    maxLength = len(max(*table, key=len))

    for row in table:
        if len(row) < maxLength:
            row.extend([''] * (maxLength - len(row)))

    table = [[row[i] for row in table] for i in range(len(table[0]))]
    table = [[item for item in column if item.strip() != ''] for column in table]

    return table

@returnList
def exportDates_():
    table = get(DATETIMES_RANGE)
    users = getUsers()
    
    table = transpose(table)

    sleepColumns = table[::2]
    wakeUpColumns = table[1::2]
            

    for user, wakeupDatesList, sleepDatesList in zip(users, wakeUpColumns, sleepColumns):
        maxIndex = min(len(wakeupDatesList), len(sleepDatesList))

        yield {
            'user': user, 
            'wakeup': wakeupDatesList[:maxIndex], 
            'sleeptime': sleepDatesList[:maxIndex]
        }

if __name__ == '__main__':
    from tools import writeFile
    from json import dumps

    writeFile('export_output.json', dumps(dict(array=exportDates_()), ensure_ascii=False))