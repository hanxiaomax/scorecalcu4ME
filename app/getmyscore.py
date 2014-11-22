from flask import Flask,request,jsonify
from app import db
from models import User, ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_KNOWN

def _getmyscore():
    # do not need to get campID from request
    # print request.args.get('query')
    campID = request.args.get('campID', type=str)
    # print campID
    user=User.get_user(campID)
    jsondict={}
    _score_items=user.score_items.all()
    #print _score_items
    print campID
    for s in _score_items:
        # print s
        jsondict={
        "page": 1,
        "total": 10,
        "rows": [
                {
                "id": s.item_name,
                "cell": {
                    "catagory": s.catagory,
                    "item_name": s.item_name,
                    "add": s.add,
                    "time": s.time,
                    "standard": s.standard,
                    "status": s.status
                }
                }
                ]
        }
    # print jsondict
    return jsonify(jsondict)
    # return "111"





