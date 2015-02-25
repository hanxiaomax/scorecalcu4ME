#coding:utf-8
from app import db
from flask import jsonify
import os

ROLE_USER = 0
ROLE_ADMIN = 1
STATUS_YES = 1
STATUS_NO = 0
STATUS_UNKNOWN= 2
OPEN=1
CLOSE=0
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True)
    campID = db.Column(db.String(120), index = True, unique = True)
    password= db.Column(db.String(120), index = True)
    grade= db.Column(db.String(64),index = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    score_items = db.relationship('Score_items', backref = 'student', lazy = 'dynamic')
    public_items= db.relationship('Excelmap', backref = 'teacher', lazy = 'dynamic')
    score=db.Column(db.Float,default=0.0)




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
    def get_user_byID(cls,id):
        user = cls.query.filter(db.or_(User.id==id)).first()
        if not user:
            return None
        return user



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
    def scoreInfo4SomeOne(cls,campID,is_jsonify=True,get_all=True):
        """get someone's score_items by campID,return as json or dict,
            scoreInfo4SomeOne["items"] contains all the infor about the score_items
            as a list
        """
        scoreInfoDict={
        "campID":campID,
        "items":[]
        }
        user=User.get_user(campID)
        if user and user.role==ROLE_USER:
            items=user.score_items.all()
            for item in items:
                scoreInfoDict["items"].append(cls.getItemInfo(item))
            has_reslut=True
        else:
            has_reslut=False
        if  has_reslut and is_jsonify :
            return jsonify(scoreInfoDict)
        elif has_reslut:
            return scoreInfoDict
        else:
            return "No user found"

    @classmethod
    def getItemInfo(cls,item):
        "get one score_items info return as a dict"

        data={
                "id":item.id,
                "catagory": item.catagory,
                "name":item.student.name,
                "item_name": item.item_name,
                "add": item.add,
                "time": cls._setTime(item.time_st,item.time_ed),
                "applytime": item.applytime,
                "status":cls._getStatus(item),
                "certification": cls._isUploaded(item),
                "uuid":item.uuid,
                "note":item.explanation
        }
        return data

    @classmethod
    def _setTime(self,time_start,time_end):
        if time_start == time_end:
            return time_start
        else:
            return time_start+u"至"+time_end


    @classmethod
    def _isUploaded(cls,item):
        if item.picpath is not None:
            return u"已上传"
        else:
            return u"无"
    @classmethod
    def _getStatus(cls,item):
        _status=item.status
        if _status==2:
            return u"未审核"
        elif _status==1:
            return u"通过"
        else:
            return u"驳回"

    @classmethod
    def addstudent(cls,campID,name,grade):

        u=User(campID=campID,
                    name=name,
                    grade=grade,
                    password=campID,
                    role=0,score=0.0)
        db.session.add(u)
        db.session.commit()

    @classmethod
    def delete(cls,campID):
        u=cls.query.filter(campID==cls.campID).first()
        db.session.delete(u)
        db.session.commit()


    @classmethod
    def edit(cls,id,campID,name,grade):

        u=cls.query.filter(id==cls.id).first()
        if User.get_user(campID):
            return u"该学号已经存在"
        else:
            # print u
            u.name=name
            u.campID=campID
            u.grade=grade
            db.session.commit()
            return u"修改成功"


class Score_items(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    catagory = db.Column(db.String(140))
    item_name= db.Column(db.String(120))
    time_st = db.Column(db.String(30))
    time_ed = db.Column(db.String(30))
    add=db.Column(db.Float)
    applytime=db.Column(db.String(30))#need to save a formated string
    status= db.Column(db.SmallInteger, default = STATUS_UNKNOWN)
    picpath=db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    uuid=db.Column(db.String(64))
    explanation=db.Column(db.String(320))
    #unicode 下汉字是3个字符

    #实现Score_items对象下标访问
    def __getitem__(self, key):
        if key=="catagory":
            return self.catagory
        elif key=="applytime":
            return self.applytime
        elif key=="status":
            return self.status
        elif key=="add":
            return self.add
        elif key=="item_name":
            return self.item_name



    def __repr__(self):
        return '<Score id=%r status=%r >' % (self.id,self.status)

    @classmethod
    def delete(cls,id):
        s=cls.query.filter(id==cls.id).first()
        db.session.delete(s)
        db.session.commit()



class Excelmap(db.Model):
    """Excelmap表的结构"""
    id = db.Column(db.Integer, primary_key = True)
    Excelname = db.Column(db.String(140))
    creater=db.Column(db.String(20))
    creater_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_time=db.Column(db.String(20))
    end_time=db.Column(db.String(20))
    creater_time=db.Column(db.DateTime)
    filepath=db.Column(db.String(140))
    status=db.Column(db.SmallInteger)
    grade= db.Column(db.String(64),index = True)

    def __repr__(self):
        return '<Excelmap %r>' % (self.id)

    @classmethod
    def getExcelLits(cls):
        items=Excelmap.query.all()
        excellist={
        "excellist":[]
        }
        for item in items:
            if item.status:
                _status="正在公示"
            else:
                _status="停止公示"
            data={
                        "id":item.id,
                        "Excelname": item.Excelname,
                        "creater":item.creater,
                        "time":item.start_time+u"至"+item.end_time,
                        "creater_time": item.creater_time,
                        "filepath": item.filepath,
                        "status":_status,
                        "grade":item.grade
                }

            excellist["excellist"].append(data)

        return jsonify(excellist)

    @classmethod
    def deleteExcel(cls,excelID):
        e=cls.query.filter(cls.id==excelID).first()
        os.remove(e.filepath)
        db.session.delete(e)
        db.session.commit()


class Grade(db.Model):
    """docstring for grade"""
    id = db.Column(db.Integer, primary_key = True)
    grade_name = db.Column(db.String(20))


    @classmethod
    def add(cls,new_grade):
        _g=Grade(grade_name=new_grade)

        db.session.add(_g)
        db.session.commit()

    @classmethod
    def remove(cls,grade_name):
        _g=cls.query.filter(grade_name==grade_name).first()
        db.session.delete(_g)
        db.session.commit()

    @classmethod
    def get_grades(cls):
        gradelist=[grade.grade_name for grade in Grade.query.all()]
        return sorted(gradelist, cmp=Grade.my_cmp)

    @classmethod
    def my_cmp(cls,a, b):
        if a[0]==b[0]:
            return cmp(a, b)
        elif a[0]==u'博' or (a[0]==u'硕' and b[0]!=u'博'):
            return 1
        else:
            return -1

