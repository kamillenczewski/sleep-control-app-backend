from database_management import database
from tools import getArgs

def getNameFromId(user_id):
    return (
        database
            .table('users')
            .select('id,name')
            .eq('id', user_id)
            .execute().data[0]['name']
    )

def execute(user_id):
    options = (
        database
            .table('bar_color_options')
            .select('owner_id,option_user_id,color,is_active')
            .eq('owner_id', user_id)
            .execute().data
    )

    data = [
        {
            'userName': getNameFromId(record['option_user_id']),
            'userId': record['option_user_id'],
            'hexColor': record['color'],
            'isActive': record['is_active'],
        }
        for record
        in options
    ]

    return data

def endpoint():
    args, isAnyNull = getArgs(
        names=['user_id'], 
        conversions=[int]
    )
    
    if isAnyNull:
        return

    return execute(*args)