#coding:utf-8
from flask import request,jsonify
from app import db
from models import User, Score_items,STATUS_YES , STATUS_NO , STATUS_UNKNOWN
from flexgrid import sorter,pageslicer

"""
教师审核页面，flexgrid获取数据所需函数
"""

def _getreview(grade="All"):
    """获取当前页内容"""
    page=request.args.get("page",type=int)#接收当前页。并非从param返回，是控件自动传递的
    rp=request.args.get("rp",type=int)
    sortcol=request.args.get('sortname')#获取要排序的行
    sorttype=request.args.get('sortorder')#获取排序方式

    if grade=="All":
        _score_items=Score_items.query.filter(Score_items.status==2).all()
    else :
        #按照年级来返回需要审核的内容
        _score_items=Score_items.query.filter(db.and_(Score_items.status==2,User.get_user_byID(Score_items.user_id).grade==grade)).all()

    _score_items_af=sorter(_score_items,sortcol,sorttype)
    return jsonify(pageslicer(page,rp,_score_items_af))

def _accpet():
    """通过按钮"""
    accept=request.args.get('accept',type=int)
    s=Score_items.query.filter(Score_items.id==accept).first()#should use first()
    s.status=STATUS_YES
    db.session.commit()
    return " "


def _reject():
    """拒绝按钮"""
    reject=request.args.get('reject',type=int)
    s=Score_items.query.filter(Score_items.id==reject).first()
    s.status=STATUS_NO
    db.session.commit()
    return " "


