#coding:utf-8
from flask import Flask,request,jsonify
from app import db,appME
from models import User, ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN,Score_items
import os
from datetime import datetime


def _getmyscore(user):
    _score_items=user.score_items.all()
    page=request.args.get("page",type=int)#接收当前页。并非从param返回，是控件自动传递的
    rp=request.args.get("rp",type=int)
    total=len(_score_items)

    jsondict={
        "page": page,#当前页
        "total": total,#总数
        "rows": []
        }

    #page:1 rows=1-->10
    #page:2 rows=10-->20

    if page*rp-1<total :
        end=page*rp
    else:
        end=total#防止越界

    for i in xrange((page-1)*rp,end):
        s=_score_items[i]
        data={
                "id": s.item_name,
                "cell": User.getItemInfo(s)
            }
        jsondict["rows"].append(data)

    return jsonify(jsondict)

def _deleteapply(user):
    Delete=request.args.get('Delete',type=int)

    _score_items=user.score_items.all()
    canDelete="No"
    for s in _score_items:
        if (s.id==Delete and s.status!=STATUS_YES):
            canDelete="Yes"
            if s.picpath is not None :
                os.remove(appME.config['UPLOAD_FOLDER']+s.uuid+".jpg")
            db.session.delete(s)
    db.session.commit()
    return canDelete


def _getTotal(user):


    _score_items=user.score_items.all()
    total=0.0
    for s in _score_items:
        if (s.status==STATUS_YES):
            if s.add is not None:
                total+=s.add
    #TODO:should move to another place
    #this works only when user login again
    user.score=total
    db.session.commit()
    return str(total)
