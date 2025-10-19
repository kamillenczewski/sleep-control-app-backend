from database_management import database
from google_sheets_export import exportDates_ as exportDates
from constants import USERS_TABLE, SLEEPING
from extended_list import List
from datetime import datetime
from satisfaction_export import exportSatisfaction

def getIdFromName(userName):
    data = database \
        .table(USERS_TABLE) \
        .select('id,name') \
        .eq('name', userName) \
        .execute().data   
    
    return List(data).first()['id']


def deleteRecordsFrom(table):
    database \
        .table(table) \
        .delete() \
        .neq('id', -1) \
        .execute()   

def normalizeDatetime(string):
    return datetime.strptime(string, "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S")

def createSleepTimesRecords(user_id, sleepStart, sleepEnd):
    sleepTimes = list(zip(sleepStart, sleepEnd))
    sleepTimes = [(normalizeDatetime(sleepStart), normalizeDatetime(sleepEnd)) for sleepStart, sleepEnd in sleepTimes]
    data = [{'user_id': user_id, 'start': sleeptime, 'end': wakeup} for sleeptime, wakeup in sleepTimes]
    return data

def datetimeToSatisfactionEndDate(string):
    return datetime.strptime(string, "%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y")

def addDatetimes(user_id, sleepStart, sleepEnd, satisfaction):
    sleepRecords = createSleepTimesRecords(user_id, sleepStart, sleepEnd)
    sleepRecords = {datetimeToSatisfactionEndDate(sleepRecord['end']): sleepRecord for sleepRecord in sleepRecords}

    for record in satisfaction:
        if record['endDate'] not in sleepRecords:
            continue

        sleepRecords[record['endDate']]['satisfaction'] = record['satisfaction']

    sleepRecords = list(sleepRecords.values())

    return (
        database
            .table(SLEEPING)
            .insert(sleepRecords)
            .execute().data  
    ) 

def fromGoogleSheetsToDatabase():
    deleteRecordsFrom(SLEEPING)

    exported = exportDates()
    userIds = [getIdFromName(record['user']) for record in exported]
    satisfactionRecords = exportSatisfaction()

    for userId, record, satisfaction in zip(userIds, exported, satisfactionRecords):
        addDatetimes(userId, record['sleeptime'], record['wakeup'], satisfaction)

if __name__ == '__main__':
    fromGoogleSheetsToDatabase()