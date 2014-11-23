from flask import Flask,request
from app import db
from models import User, Score_items,ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN
import datetime


def _saveapply():
    _catagory = request.args.get('catagory', type=unicode)#should be unicode,if it is str than we will get None
    _name = request.args.get('name', type=unicode)
    _campID = request.args.get('campID', type=str)

    user=User.get_user(_campID)
    s=Score_items(catagory=_catagory,
        item_name=_name,
        time=datetime.datetime.today(),
        student=user)
    print datetime.datetime.today()
    db.session.add(s)
    db.session.commit()
    return ""
