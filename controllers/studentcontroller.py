from flask import Response
import re
from config.database import db
import json
from bson.json_util import dumps
from app import app

@app.route("/student/all")
def allStudents():
    cursor=db.Users.find({}, {'_id': False, 'labs': False})

    data = dumps(cursor)
    resp = Response(data, status=200, mimetype='application/json')
    return resp



@app.route("/student/create/")
@app.route("/student/create/<studentname>")
def createStudent(studentname=None):
    '''
    Create student if it wasn't in database and returns it
    '''
    query = {"name": studentname}
    if db.Users.find_one(query):
        data = dumps({"Error": "El usuario ya existe"})
        return Response(data, status=409, mimetype='application/json')

    data = dumps(db.Users.insert_one({"name": studentname, "labs": []}).inserted_id)
    return Response(data, status=200, mimetype='application/json')