from google_sheets_api import get
from tools import returnList
from database_management import database
from constants import USERS_TABLE
from extended_list import List

SHEET_NAME = 'Satisfaction'
USERS_RANGE = f'{SHEET_NAME}!1:1'
DATETIMES_RANGE = f'{SHEET_NAME}!A:A'
SATISFACTION_RANGE = f'{SHEET_NAME}!B2:E'
 
def getUsers():
    return [name.strip() for name in get(USERS_RANGE)[0] if name.strip() != '']

def getIdFromName(userName):
    data = database \
        .table(USERS_TABLE) \
        .select('id,name') \
        .eq('name', userName) \
        .execute().data   
    
    return List(data).first()['id']

@returnList
def getUserIds():
    for user in getUsers():
        yield getIdFromName(user)

def fillTable(table):
    maxLength = len(max(*table, key=len))

    for row in table:
        if len(row) < maxLength:
            row.extend([''] * (maxLength - len(row)))

    return table

def transpose(table):
    table = fillTable(table)
    table = [[row[i] for row in table] for i in range(len(table[0]))]
    return table

@returnList
def getRecords(satisfaction, dates, userIds):
    for satisfactionArray, userId in zip(satisfaction, userIds):
        yield [
            {'satisfaction': satisfactionPercent, 'user_id': userId, 'endDate': date}
            for date, satisfactionPercent 
            in zip(dates, satisfactionArray)
            if satisfactionPercent.strip() != ''
        ]

@returnList
def exportSatisfaction():
    satisfaction = transpose(get(SATISFACTION_RANGE))
    dates = transpose(get(DATETIMES_RANGE)[1:])[0]
    userIds = getUserIds()

    records = getRecords(satisfaction, dates, userIds)

    return records
