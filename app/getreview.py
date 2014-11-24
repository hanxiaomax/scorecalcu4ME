#coding:utf-8
from flask import Flask,request,jsonify
from app import db
from models import User, Score_items,ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN
#TODO:should i make teacher search what have been approve and reject?
def _getreview():
    #campID = request.args.get('campID', type=str)
    jsondict={
        "page": 1,
        "total": 100,
        "rows": []
        }
    _score_items=Score_items.query.filter(Score_items.status==2)
    #TODO:maybe filter when query from the db? ----DOWN
    for s in _score_items:
        data={
                "id": s.item_name,
                "cell": {
                    "id":s.id,
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

def _accpet():
    print "_accpet"
    accept=request.args.get('accept',type=int)
    print accept
    s=Score_items.query.filter(Score_items.id==accept).first()#should use first()
    s.status=STATUS_YES
    db.session.commit()
    return " "


def _reject():
    print "_reject()"
    reject=request.args.get('reject',type=int)
    s=Score_items.query.filter(Score_items.id==reject).first()
    print s
    s.status=STATUS_NO
    db.session.commit()
    return " "
