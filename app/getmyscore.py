from flask import Flask,request,jsonify
from app import db
from models import User, ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_KNOWN

def _getmyscore():
    campID = request.args.get('campID', type=str)
    user=User.get_user(campID)
    jsondict={}
    _score_items=user.score_items.all()
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

    return jsonify(jsondict)





