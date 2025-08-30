from flask import Flask
from endpoint_registry import EndpointRegistry
from tools import createPath, logEndpoints, writeFile
from javascript_backend_builder import createBackendInFrontend
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
registry = EndpointRegistry(app)

registry.registerEndpointsFromFolder(createPath('endpoints'))

logEndpoints(app, 'endpoints-log.txt')
writeFile('fronted-backend.txt', createBackendInFrontend(registry.modules, registry.endpoints))


if __name__ == '__main__':
    app.run()



