#coding:utf-8
from flask import Flask,request,jsonify
from app import db,appME
from models import User, ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN
import os

def _getmyscore():
    campID = request.args.get('campID', type=str)
    print campID
    user=User.get_user(campID)
    jsondict={
        "page": 1,
        "total": 100,
        "rows": []
        }
    _score_items=user.score_items.all()
    for s in _score_items:
        _status=s.status
        if _status==2:
            _status=u"未审核"
        elif _status==1:
            _status=u"通过"
        else:
            _status=u"驳回"
        data={
                "id": s.item_name,
                "cell": {
                    "id":s.id,
                    "catagory": s.catagory,
                    "item_name": s.item_name,
                    "add": s.add,
                    "time": s.time,
                    "standard": s.standard,
                    "status": _status
                }
            }

        jsondict["rows"].append(data)
    return jsonify(jsondict)

def _deleteapply():
    Delete=request.args.get('Delete',type=int)
    campID = request.args.get('campID', type=str)
    user=User.get_user(campID)
    _score_items=user.score_items.all()
    canDelete="No"
    for s in _score_items:
        if (s.id==Delete and s.status!=STATUS_YES):
            canDelete="Yes"
            if s.picpath is not None :
                os.remove(appME.config['UPLOAD_FOLDER']+"certiID"+str(s.id)+".png")
            db.session.delete(s)
    db.session.commit()
    return canDelete


def _getTotal():
    campID = request.args.get('campID', type=str)
    user=User.get_user(campID)
    _score_items=user.score_items.all()
    total=0
    for s in _score_items:
        if (s.status==STATUS_YES):
            if s.add is not None:
                total+=int(s.add)
    user.score=total
    db.session.commit()
    return str(total)
