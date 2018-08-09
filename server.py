import api
from flask import Flask
from flask_restful import Api

app = Flask(__name__)

app.config.update({'SECRET_KEY': 'A0Zr98j/3yX R~XHH!jmN]LWX/,?dffRT', 'STATIC_FOLDER': '/static'})

restful_api = Api(app)
restful_api.add_resource(api.MainHandler, *[r"/oauth", r"/oauth2callback"])
restful_api.add_resource(api.MountsHandler, r"/mounts")

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
