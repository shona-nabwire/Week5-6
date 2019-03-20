from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity

from diary import Diary, Entry

app = Flask(__name__)
app.secret_key = 'nshie'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Entry, '/entry/<string:entryid>')
api.add_resource(Diary, '/entries')

if __name__ == '__main__':
    app.run(port=5000, debug=True)