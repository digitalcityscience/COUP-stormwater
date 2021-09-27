from flask_cors import CORS, cross_origin
from endpoints import app

# Description
# This file is only to be executed for development purpose. It provides more debugging (maybe also sensitive) ]
# informations. For production please use it with gunicorn (see entrypoint.sh)

if __name__ == '__main__':
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.run(host='0.0.0.0', port=5002, debug=True)
