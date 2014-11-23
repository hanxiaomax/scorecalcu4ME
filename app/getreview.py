#coding:utf-8
from flask import Flask,request,jsonify
from app import db
from models import User, Score_items,ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN

def _getreview():
    #campID = request.args.get('campID', type=str)
    jsondict={
        "page": 1,
        "total": 100,
        "rows": []
        }
    users=User.query.all()
    print users
    for user in users:
        _score_items=user.score_items.all()#TODO:maybe filter when query from the db?
        for s in _score_items:
            _status=s.status
            if _status==2:
                data={
                        "id": s.item_name,
                        "cell": {
                            "name":s.student.name,
                            "catagory": s.catagory,
                            "item_name": s.item_name,
                            "add": s.add,
                            "time": s.time,
                            "standard": s.standard,
                            "certification": ""
                        }
                    }
                jsondict["rows"].append(data)



    return jsonify(jsondict)





