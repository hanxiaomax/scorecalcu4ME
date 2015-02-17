#coding:utf-8
from flask import Flask,request,g
from app import db
from models import User, Score_items,ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN
import datetime
import json
import os
basedir=os.path.abspath(os.path.dirname(__file__))
#TODO:should move this to client?
def getvalue(cat,name):
    f=file(basedir+"/static/select.json")
    s=json.load(f)
    f.close()
    for val in s:
        if val["catagory"]==cat:
            for v in val["subcatagory"]:
                if v["name"]==name:
                    return v["value"]


def _saveapply(filepath=False):
    #by default we think there is no pic being uploaded
    _catagory = request.args.get('catagory', type=unicode)#should be unicode,if it is str than we will get None
    _name = request.args.get('name', type=unicode)
    _campID = request.args.get('campID', type=str)
    _time_st=request.args.get('time_st',type=unicode)#should get a unicode
    _time_ed=request.args.get('time_ed',type=unicode)#should get a unicode
    # _time=_time.decode('utf-8')
    # print datetime.datetime.strptime(_time, '%Y-%m-%d')
    _applytime=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')#format the timestamp return as a string
    _add=getvalue(_catagory,_name)
    _uuid=request.args.get('UUID', type=str)
    _pic=request.args.get('pic',type=str)#if pic uploaded
    _explanation=request.args.get('explanation',type=unicode)

    user=User.get_user(_campID)



    s=Score_items(catagory=_catagory,
        item_name=_name,
        time_st=_time_st,
        time_ed=_time_ed,
        add=_add,
        applytime=_applytime,
        student=user,
        uuid=_uuid,
        explanation=_explanation,
        )

    db.session.add(s)
    db.session.flush()
    if _pic=="true":
        s.picpath=basedir+"/uploads/"+_uuid+".jpg"
    elif _pic=="false":
        s.picpath=None
    db.session.commit()

    return ""

