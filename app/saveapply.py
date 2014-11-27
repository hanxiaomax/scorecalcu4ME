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

def getstandard():
    pass

def _saveapply(filepath):
    _catagory = request.args.get('catagory', type=unicode)#should be unicode,if it is str than we will get None
    _name = request.args.get('name', type=unicode)
    _campID = request.args.get('campID', type=str)
    _time=request.args.get('time',type=str)
    _add=getvalue(_catagory,_name)
    user=User.get_user(_campID)

    _standard="2013-9-4"

    s=Score_items(catagory=_catagory,
        item_name=_name,
        time=_time,
        add=_add,
        standard=_standard,
        student=user)

    db.session.add(s)
    #execute SQL so you can get id
    db.session.flush()
    new_id=s.id
    db.session.commit()
    uploadDir=os.path.dirname(filepath)
    #rename the pic ,dont forget the dirpath
    #os.rename(filepath,uploadDir+"/"+_campID+"_No"+str(new_id)+".png")
    os.rename(filepath,uploadDir+"/"+"certiID"+str(new_id)+".png")

    return ""

