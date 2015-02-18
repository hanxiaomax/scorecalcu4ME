#coding:utf-8
from flask import Flask,request,jsonify
from app import db
from models import User, Score_items,ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN
#TODO:should i make teacher search what have been approve and reject?
def _getreview(grade="All"):
    jsondict={
        "page": 1,
        "total": 100,
        "rows": []
        }
    if grade=="All":
        _score_items=Score_items.query.filter(Score_items.status==2)
    else :
        #按照年级来返回需要审核的内容
        _score_items=Score_items.query.filter(db.and_(Score_items.status==2,User.get_user_byID(Score_items.user_id).grade==grade))
    for s in _score_items:
        data={
                "id": s.item_name,
                "cell": User.getItemInfo(s)
            }
        jsondict["rows"].append(data)

    return jsonify(jsondict)

def _accpet():
    accept=request.args.get('accept',type=int)
    s=Score_items.query.filter(Score_items.id==accept).first()#should use first()
    s.status=STATUS_YES
    db.session.commit()
    return " "


def _reject():
    reject=request.args.get('reject',type=int)
    s=Score_items.query.filter(Score_items.id==reject).first()
    s.status=STATUS_NO
    db.session.commit()
    return " "

if __name__ == '__main__':
    _getreview(grade=u"硕2012")
