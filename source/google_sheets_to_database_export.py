from database_management import database
from google_sheets_export import exportDates
from constants import DATES_TABLE, USERS_TABLE
from extended_list import List

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

def addDatetimes(userId, wakeupDatetimes, sleeptimeDatetimes):
    dataToInser = \
        [{ 'user_id': userId, 'type': 'wakeup', 'datetime': date } for date in wakeupDatetimes] + \
        [{ 'user_id': userId, 'type': 'sleeptime', 'datetime': date } for date in sleeptimeDatetimes]
    
    # dates1 => dates
    return database \
        .table('dates1') \
        .insert(dataToInser) \
        .execute().data   

def fromGoogleSheetsToDatabase():
    deleteRecordsFrom(DATES_TABLE)

    exported = exportDates()

    userIds = [getIdFromName(record['user']) for record in exported]

    for userId, record in zip(userIds, exported):
        addDatetimes(userId, record['wakeup'], record['sleeptime'])

if __name__ == '__main__':
    fromGoogleSheetsToDatabase()