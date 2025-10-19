from flask import Flask, request, jsonify
from endpoint_registry import EndpointRegistry
from tools import createPath, logEndpoints, writeFile, log
from javascript_backend_builder import createBackendInFrontend
from flask_cors import CORS
from secret_loader import SecretLoader

app = Flask(__name__)   
CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers=["token", 'Content-Type'])
registry = EndpointRegistry(app)

@app.before_request
def validateKey():
    if request.method == "OPTIONS":
        return

    log(request.headers)

    possibleKey = request.headers.get("token")
    key = SecretLoader.get("FRONTEND_TOKEN")

    if possibleKey != key:
        return jsonify({"error": "Unauthorized"}), 401



registry.registerEndpointsFromFolder(createPath('endpoints'))

logEndpoints(app, 'endpoints-log.txt')
writeFile('fronted-backend.txt', createBackendInFrontend(
    registry.modules, 
    registry.endpoints,
    registry.methods
))


if __name__ == '__main__':
    app.run()



