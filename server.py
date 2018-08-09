import api
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
restful_api = Api(app)
restful_api.add_resource(api.MainHandler, *[r"/", r"/oauth2callback"])

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
