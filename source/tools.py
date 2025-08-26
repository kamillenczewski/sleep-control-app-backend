from flask import request
from os.path import join
from constants import MAIN_PATH, LOG_PATH, SECRET_PATH
from dotenv import load_dotenv
from os import getenv

# defaults to remove, check references
def getArgs(names, defaults=None, conversions=None):
    if not isinstance(defaults, list):
        defaults = [defaults for _ in names]

    if not isinstance(conversions, list):
        conversions = [conversions for _ in names]

    values = [request.args.get(name, defaultValue) for name, defaultValue in zip(names, defaults)]

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

def log(text):
    with open(LOG_PATH, 'a+') as file:
        file.write(text + '\n')

def loadSecret():
    load_dotenv(SECRET_PATH)

def getSecret(name):
    return getenv(name)