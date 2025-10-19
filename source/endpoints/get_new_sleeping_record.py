from tools import getArgs
# from database_management import database

def execute(user_id):
    # data = (
    #     database
    #         .table('sleeping')
    #         .upsert([{'user_id': user_id}])
    #         .execute().data
    # )

    return [{'user_id': user_id, 'start': None, 'end': None, 'satisfaction': None}]


methods = [
    'POST'
]

def endpoint():
    args, isAnyNull = getArgs(
        names=['user_id'], 
        conversions=[int],
        methods=methods
    )
    
    if isAnyNull:
        return

    return execute(*args)