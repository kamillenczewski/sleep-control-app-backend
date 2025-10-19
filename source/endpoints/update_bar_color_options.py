from tools import getArgs
from database_management import database

# owner_id, option_user_id, color, is_active
def execute(user_id, options):
    optionsWithUserId = [
        {
            'owner_id': user_id, 
            'option_user_id': option['userId'],
            'color': option['hexColor'],
            'is_active': option['isActive'],
        } 
        for option 
        in options
    ]

    data = (
        database
            .table('bar_color_options')
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