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

print(execute(16, [
    {}
]))