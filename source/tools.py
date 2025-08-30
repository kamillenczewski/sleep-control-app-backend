from flask import request
from os.path import join
from constants import MAIN_PATH, LOG_PATH
from datetime import datetime

def getArgsFromGETRequest(names):
    return [request.args.get(name, None) for name in names]

def getArgsFromPOSTRequest(names):
    data = request.get_json()
    data = [data.get(name) for name in names]
    return data

def getArgs(names, conversions=None, methods=None):
    if methods and methods[0] == 'POST':
        values = getArgsFromPOSTRequest(names)
    else:
        values = getArgsFromGETRequest(names)

    if not isinstance(conversions, list):
        conversions = [conversions for _ in names]

    isAnyNull = any(value == None for value in values)

    if isAnyNull:
        return [], isAnyNull

    values = [conversion(value) if conversion else value for value, conversion in zip(values, conversions)]

    return values, isAnyNull
        

def returnList(func):
    def _(*args, **kwargs):
        return list(func(*args, **kwargs))
    
    return _

@returnList
def transpose(matrix):
    for i in range(len(matrix[0])):
        yield [row[i] for row in matrix]

def writeFile(path, content):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)

def readFile(path):
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()
    
def createPath(path):
    return join(MAIN_PATH, path)

def logEndpoints(app, destination):
    with open(destination, 'w') as file:
        for rule in app.url_map.iter_rules():
            file.write(f"{rule.endpoint}: {rule.rule}\n")

def log(*parts):
    preText = datetime.now().__str__()

    with open(LOG_PATH, 'a+') as file:
        file.write(preText + ' ' + ' '.join(map(str, parts)) + '\n')

def printList(items):
    print('\n'.join(map(str, items)))