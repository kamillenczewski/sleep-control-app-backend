from flask import Flask
from endpoint_registry import EndpointRegistry
from tools import createPath, logEndpoints, writeFile, loadSecret
from javascript_backend_builder import createBackendInFrontend

loadSecret()

app = Flask(__name__)
registry = EndpointRegistry(app)

registry.registerEndpointsFromFolder(createPath('endpoints'))

logEndpoints(app, 'endpoints-log.txt')
writeFile('fronted-backend.txt', createBackendInFrontend(registry.modules, registry.endpoints))

if __name__ == '__main__':
    app.run()