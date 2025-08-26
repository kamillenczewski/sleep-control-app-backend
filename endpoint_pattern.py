from tools import getArgs

def execute():
    pass

def endpoint():
    args, isAnyNull = getArgs(
        names=['arg1', 'arg2', 'arg3'], 
        defaults=None,
        conversions=[convert1, convert2, convert3]
    )
    
    if isAnyNull:
        return

    return execute(*args)