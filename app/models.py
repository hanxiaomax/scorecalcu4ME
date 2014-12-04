#coding:utf-8
from app import db
from flask import jsonify

ROLE_USER = 0
ROLE_ADMIN = 1
STATUS_YES = 1
STATUS_NO = 0
STATUS_UNKNOWN= 2
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True)
    campID = db.Column(db.String(120), index = True, unique = True)
    password= db.Column(db.String(120), index = True)
    grade= db.Column(db.String(64),index = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    score_items = db.relationship('Score_items', backref = 'student', lazy = 'dynamic')
    score=db.Column(db.String(10),default="0")

    def __repr__(self):
        return '<User %r>' % (self.name)

    def is_authenticated(self):
        return True

    def is_active(self):
        #Returns True if this is an active user
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @classmethod
    def login_check(cls,user_name,password):
        # print user_name
        user = cls.query.filter(db.and_(User.campID==user_name, User.password==password)).first()
        # print user
        if not user:
            return None
        return user

    @classmethod
    def get_user(cls,campID):
        "get user by campID"
        user = cls.query.filter(db.or_(User.campID==campID)).first()
        if not user:
            return None
        return user

    @classmethod
    def userInfo(cls,campID,is_jsonify=True):
        "get all the infomation about user return as a dict"
        userInfoDict={}
        user = cls.get_user(campID)

        _name = user.name
        _campID = user.campID
        _grade = user.grade
        _score = user.score
        userInfoDict={
         "name" : user.name,
        "campID" : user.campID,
        "grade" : user.grade,
        "sum" : user.score,
        "items":cls.scoreInfo4SomeOne(campID,is_jsonify=False)["items"]
        }  
        print userInfoDict
        if is_jsonify:
            return  jsonify(userInfoDict)
        else:
            return userInfoDict

    @classmethod
    def scoreInfo4SomeOne(cls,campID,is_jsonify=True,get_all=True):

        scoreInfoDict={
        "campID":campID,
        "items":[]
        }
        user=User.get_user(campID)
        if user and user.role==ROLE_USER:
            items=user.score_items.all()
            for item in items:
                _status=item.status
                if _status==2:
                    _status=u"未审核"
                elif _status==1:
                    _status=u"通过"
                else:
                    _status=u"驳回"
                data={
                        "id":item.id,
                        "catagory": item.catagory,
                        "item_name": item.item_name,
                        "add": item.add,
                        "time": item.time,
                        "applytime": item.applytime,
                        "status":_status
                }
                scoreInfoDict["items"].append(data)
            has_reslut=True
        else:
            has_reslut=False
            
        if  has_reslut and is_jsonify :
            return jsonify(scoreInfoDict)
        elif has_reslut:
            print scoreInfoDict["items"]
            return scoreInfoDict
        else:
            return "No user found"


class Score_items(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    catagory = db.Column(db.String(140))
    item_name= db.Column(db.String(120))
    time = db.Column(db.String(140))
    add=db.Column(db.Integer)
    applytime=db.Column(db.String(30))#need to save a formated string
    status= db.Column(db.SmallInteger, default = STATUS_UNKNOWN)
    picpath=db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Score %r>' % (self.time)

    
