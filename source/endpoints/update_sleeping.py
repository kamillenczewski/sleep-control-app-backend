from tools import getArgs
from database_management import database

def execute(user_id, sleeping_data):
    data = [
        {
            **record,
            'user_id': user_id
        } 
        for record 
        in sleeping_data
        if record['start'] != None and record['end'] != None
    ]

    data = (
        database
            .table('sleeping')
            .upsert(data)
            .execute().data
    )

    return data

    

methods = [
    'POST'
]

def endpoint():
    args, isAnyNull = getArgs(
        names=['user_id', 'sleeping_data'], 
        conversions=[int, None],
        methods=methods
    )
    
    if isAnyNull:
        return

    return execute(*args)

# execute(16, [
#     {'start': '2025-09-26 23:00:32', 'end': '2025-09-27 08:06:07', 'satisfaction': 51.9}
# ])