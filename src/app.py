from flask import Flask, jsonify, json
from flask_cors import CORS, cross_origin
from flask import make_response, request, current_app
from functools import update_wrapper
import firebase_admin 
from firebase_admin import auth

default_app = firebase_admin.initialize_app()
DEBUG = True

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(__name__)

cors = CORS(app, resources={
    r"/deleteUser": {"origins": "http://localhost:port"}})
@app.route('/deleteUser', methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def deleteUser():
    response = ''
    email = ((request.args.get('email')))
    user = auth.get_user_by_email(email)
    auth.delete_user(user.uid)
    print(response)
    return ("Ok"+response)

cors = CORS(app, resources={
    r"/disableUser": {"origins": "http://localhost:port"}})
@app.route('/disableUser', methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def disableUser():
    response = ''
    email = ((request.args.get('email')))
    user = auth.get_user_by_email(email)
    auth.update_user(user.uid,
    disabled=True)
    print(response)
    return ("Ok"+response)

cors = CORS(app, resources={
    r"/activateUser": {"origins": "http://localhost:port"}})
@app.route('/activateUser', methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def activateUser():
    response = ''
    email = ((request.args.get('email')))
    user = auth.get_user_by_email(email)
    auth.update_user(user.uid,
    disabled=False)
    print(response)
    return ("Ok"+response)


# sanity check route
if __name__ == '__main__':
    app.run(port=1156)