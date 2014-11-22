from flask import Flask,request,jsonify
from app import db
from models import User, ROLE_USER, ROLE_ADMIN

def mysum():
    campID = request.args.get('page', type=str)
    user=User.get_user(campID)
    result=user.to_json()
    print result
    return jsonify(result)



