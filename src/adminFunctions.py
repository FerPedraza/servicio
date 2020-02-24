from flask import Flask, jsonify, json
from flask_cors import CORS, cross_origin
from flask import make_response, request, current_app
from functools import update_wrapper
from datetime import timedelta
import firebase_admin 
from firebase_admin import auth

DEBUG = True

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(__name__)

cors = CORS(app, resources={
    r"/deleteUser": {"origins": "http://localhost:1155"}})


@app.route('/deleteUser', methods=['GET'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def deleteUser():
    email = ((request.args.get('email')))
    default_app = firebase_admin.initialize_app()
    user = auth.get_user_by_email(email)
    auth.delete_user(user.uid)
    print('Successfully deleted user')
    return "Done"


# sanity check route
if __name__ == '__main__':
    app.run(port=1156)






