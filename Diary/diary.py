from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

entries = []

class Diary(Resource):
    def get(self):
        return{'entries': entries}

class Entry(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('info',
            type = str,
            required = True,
            help = "This field cannot be left blank!"
        )
    @jwt_required()
    def get(self, entryid):
        entry = next(filter(lambda x: x['entryid'] == entryid, entries), None)
        return {'entry': entry}, 200 if entry else 404
    
    def post(self, entryid):
        if next(filter(lambda x: x['entryid'] == entryid, entries), None):
            return {'message': "An entry with entryid '{}' already exists.".format(entryid)}, 400
        
        data = Entry.parser.parse_args()
        entry = {'entryid': entryid, 'info': data['info']}
        entries.append(entry)
        return entry, 201
    
    def delete(self, entryid):
        global entries
        entries = list(filter(lambda x:x['entryid'] != entryid, entries))
        return {'message': 'entry deleted'}

    def put(self, entryid):
        data = Entry.parser.parse_args()

        entry = next(filter(lambda x: x['entryid'] == entryid, entries), None)
        if entry is None:
            entry = {'entryid': entryid, 'info': data['info']}
            entries.append(entry)
        else:
            entry.update(data)
        return entry