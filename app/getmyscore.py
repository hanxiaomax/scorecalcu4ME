#coding:utf-8
from flask import request,jsonify
from app import db
from models import User,STATUS_YES , STATUS_NO , STATUS_UNKNOWN,Score_items
import os
from flexgrid import sorter,pageslicer

"""
学生申请页面，flexgrid获取数据所需函数
"""

def _getmyscore(user):
    """获取当前页内容"""
    page=request.args.get("page",type=int)#接收当前页。并非从param返回，是控件自动传递的
    rp=request.args.get("rp",type=int)
    sortcol=request.args.get('sortname')#获取要排序的行
    sorttype=request.args.get('sortorder')#获取排序方式
    _score_items=user.score_items.all()
    _score_items_af=sorter(_score_items,sortcol,sorttype)

    return jsonify(pageslicer(page,rp,_score_items_af))



def _deleteapply(user):
    """删除按钮"""
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
    """更新总分"""
    _score_items=user.score_items.all()
    total=0.0
    for s in _score_items:
        if (s.status==STATUS_YES):
            if s.add is not None:
                total+=s.add
    user.score=total
    db.session.commit()
    return str(total)


