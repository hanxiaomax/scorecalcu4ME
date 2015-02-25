#coding:utf-8
from flask import Flask,request,jsonify
from app import db,appME
from models import User, ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN,Score_items
import os
from datetime import datetime
import json


# sortcol=request.args.get('sortname')#获取要排序的行
# sorttype=request.args.get('sortorder')#获取排序方式
# print sortcol
# print sorttype

def mycmp(a,b):
    if a>b:
        return 1
    else:
        return -1

def sorter(before_sort,col,method):
    after_sort=sorted(before_sort,cmp=mycmp,key=lambda s:s[col],reverse=True if method=="asc" else False)
    return after_sort


def pageslicer(page,rp,_score_items):
    total=len(_score_items)#11
    jsondict={
        "page": page,#当前页
        "total": total,#总数
        "rows": []
        }
    for i in xrange((page-1)*rp,(page*rp if page*rp-1<total else total)):
        s=_score_items[i]

        data={
                "id": s.item_name,
                "cell": User.getItemInfo(s)
            }
        jsondict["rows"].append(data)

    return jsondict




def _getmyscore(user):
    page=request.args.get("page",type=int)#接收当前页。并非从param返回，是控件自动传递的
    rp=request.args.get("rp",type=int)
    sortcol=request.args.get('sortname')#获取要排序的行
    sorttype=request.args.get('sortorder')#获取排序方式
    _score_items=user.score_items.all()
    _score_items_af=sorter(_score_items,sortcol,sorttype)

    return jsonify(pageslicer(page,rp,_score_items_af))






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


