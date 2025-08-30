from tools import getArgs, log
from database_management import database

# option_id, user_id, value
def execute(user_id, options):
    optionsWithUserId = [
        {
            'user_id': user_id, 
            'option_id': option['option_id'],
            'value': option['value']
        } 
        for option 
        in options
        if option['value'] is not None
    ]

    data = (
        database
            .table('users_and_options')
            .upsert(optionsWithUserId)
            .execute().data
    )

    return data

    

methods = [
    'POST'
]

def endpoint():
    args, isAnyNull = getArgs(
        names=['user_id', 'options'], 
        conversions=[int, None],
        methods=methods
    )
    
    if isAnyNull:
        return

    return execute(*args)

