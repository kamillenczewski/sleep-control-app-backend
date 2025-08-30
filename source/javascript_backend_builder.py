from inspect import signature
from tools import returnList

def removeUnderscoresFromEndpoint(endpointName):
    parts = endpointName.split('_')
    parts = [parts[0]] + [part.title() for part in parts[1:]]
    newName = ''.join(parts)
    return newName

@returnList
def createBackendEndpointsInFrontend(modules, endpoints):
    for module, endpoint in zip(modules, endpoints):
        endpointName = removeUnderscoresFromEndpoint(endpoint)
        argNames = [name for name, _ in signature(module.execute).parameters.items()]
    
        jsArgs = '{' + ', '.join([arg + ': ' + arg for arg in argNames]) + '}'

        argNames += ['onData=null']

        head = f"export const {endpointName} = ({', '.join(argNames)}) =>"
        body = f"  fetchLink('{endpoint}', onData ? onData : _ => null, {jsArgs});"

        yield head + '\n' + body
    
def createBackendInFrontend(modules, endpoints):
    return '\n\n'.join([func for func in createBackendEndpointsInFrontend(modules, endpoints)])