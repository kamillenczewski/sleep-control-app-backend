from flask import make_response, jsonify
from types import FunctionType
from uuid import uuid4
from os import listdir
from os.path import join
from importlib.util import spec_from_file_location, module_from_spec
from tools import writeFile, log

def writeDict(path, dictionary):
    lines = []

    for key, value in dictionary.items():
        lines.append(str(key) + ': ' + str(value))

    writeFile(path, '\n'.join(lines))

def generateId():
    return uuid4().__str__().replace('-', '')

def createFunction(previousFunction):
    return FunctionType(
        previousFunction.__code__,
        previousFunction.__globals__,
        name=generateId(),
        argdefs=previousFunction.__defaults__,
        closure=previousFunction.__closure__
    )

def createResponse(result):
    try:
        response = make_response(jsonify({'result': result}))
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Exception as e:
        response = make_response(jsonify({'error': str(e)}), 400)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

class EndpointRegistry:
    def __init__(self, app):
        self.app = app
        self.linkSeparator = '/'
        self.endpointSuffix = 'Endpoint'
        self.modules = []
        self.endpoints = []
        self.methods = []

    def createLink(self, linkElements):
        return self.linkSeparator + self.linkSeparator.join(linkElements)

    def registerMainEndpoint(self, bodyMethod):
        self.app.route('/')(bodyMethod)

    def registerEndpoint(self, linkElements, resultMethod, methods=None):
        if isinstance(linkElements, str):
            linkElements = [linkElements]

        if isinstance(methods, str):
            methods = [methods]

        self.app.route(self.createLink(linkElements), methods=methods)(
            createFunction(lambda: createResponse(resultMethod()))
        )

    def registerEndpointsFromFolder(self, path, skip=['__pycache__']):
        for fileName in listdir(path):
            if fileName in skip:
                continue

            modulePath = join(path, fileName)
            moduleName = fileName.removesuffix('.py')

            moduleSpecification = spec_from_file_location(moduleName, modulePath)
            module = module_from_spec(moduleSpecification)

            moduleSpecification.loader.exec_module(module)

            if not hasattr(module, 'endpoint'):
                continue
            
            
            methods = module.methods if hasattr(module, 'methods') else None

            self.registerEndpoint(moduleName, module.endpoint, methods)

            self.modules.append(module)
            self.endpoints.append(moduleName)
            self.methods.append(methods[0] if methods else 'GET')