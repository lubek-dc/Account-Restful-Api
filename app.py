import datetime
import os
import uuid
import configparser
from functools import wraps
import jwt
from flask import Flask, request, jsonify, make_response
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

parser = configparser.ConfigParser()
parser.read('config.ini')  # You must Create config.ini file in this same directory


# config.ini file:
# [SECURITY]
# SECRET_KEY: <you can type here whatever you want for example ThisIsSecret but this will be easy to crack>

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SECRET_KEY'] = parser.get('SECURITY', 'SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
secret_key = parser.get('SECURITY', 'SECRET_KEY')
# Initialize Database
db = SQLAlchemy(app)
# Initialize Marshmallow
ma = Marshmallow(app)


# User Class/Model

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    public_id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    admin = db.Column(db.Boolean)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    message = db.Column(db.String(5000))


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, secret_key)
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator


def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, secret_key)
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
            if current_user.admin is False:
                return jsonify({'message': 'Restricted area you must be admin'})
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator


# User Schema
class UsersSchema(ma.Schema):
    class Meta:
        fields = ['id', 'public_id', 'name', 'password', 'admin']


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)


@app.route('/register', methods=['GET', 'POST'])
def signup_user():
    name = request.json['name']
    password = request.json['password']

    new_user = Users(public_id=str(uuid.uuid4()), name=name, password=password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registered successfully'})


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = Users.query.filter_by(name=auth.username).first()

    if user.password == auth.password:
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/users', methods=['GET'])
@admin_required
def get_all_users(current_user):
    allusers = Users.query.all()
    result = users_schema.dump(allusers)
    return jsonify(result)


@app.route('/user', methods=['POST', 'GET'])
@token_required
def create_author(current_user):
    data = request.get_json()

    new_authors = Users(id=data['id'], author=data['author'], message=data['message'])
    db.session.add(new_authors)
    db.session.commit()

    return jsonify({'message': 'new author created'})


# Create User
# @app.route('/user',methods=['POST'])
# def add_user():
#   id = request.json['id']
#  name = request.json['name']
# password = request.json['password']
#
#   new_user = User(id,name,password)
#
#   db.session.add(new_user)
#  db.session.commit()

# return user_schema.jsonify(new_user)
# db
# @app.route('/',methods=['GET'])
# def get():
#    return jsonify({
#        'msg': 'Hello World'
#    })

# Get all Users
# @app.route('/user', methods=['GET'])
# def get_users():
#    allusers = User.query.all()
#    result = users_schema.dump(allusers)
#    return jsonify(result)
# Run Server

if __name__ == '__main__':
    app.run(debug=True)
