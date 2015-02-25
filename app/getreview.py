#coding:utf-8
from flask import Flask,request,jsonify
from app import db
from models import User, Score_items,ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN
#TODO:should i make teacher search what have been approve and reject?
def _getreview(grade="All"):
    page=request.args.get("page",type=int)#接收当前页。并非从param返回，是控件自动传递的
    rp=request.args.get("rp",type=int)
    jsondict={
        "page": rp,
        "total": 0,
        "rows": []
        }
    if grade=="All":

        _score_items=Score_items.query.filter(Score_items.status==2).all()
    else :
        #按照年级来返回需要审核的内容
        _score_items=Score_items.query.filter(db.and_(Score_items.status==2,User.get_user_byID(Score_items.user_id).grade==grade)).all()

    total=len(_score_items)

    jsondict={
        "page": page,
        "total": total,
        "rows": []
        }
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
