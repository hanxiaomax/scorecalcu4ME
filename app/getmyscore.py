from flask import Flask,request,jsonify
from app import db
from models import User, ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_KNOWN

def _getmyscore(campID):
    #do not need to get campID from request
    user=User.get_user(campID)
    _score_items=user.score_items.all()
    jsondict={
    "page": 1,
    "total": 1,
    "rows": [
        {
            "id": "ZW",
            "cell": {
                "catagory": _score_items.catagory,
                "item_name": _score_items.item_name,
                "add": _score_items.add,
                "time": _score_items.time,
                "standard": _score_items.standard,
                "status": _score_items.status
            }
        }
    ]
}

    return jsonify(jsondict)





