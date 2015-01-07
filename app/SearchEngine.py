#coding:utf-8
from datetime import datetime,timedelta
from models import User,Score_items
from app import db
from flask import jsonify


class TimeManager(object):
    """docstring for TimeManager"""

    #把datetime对像转换为字符串形式
    def strTime(self,dbTime):
        return dbTime.strftime('%Y-%m-%d %H:%M')
    #把字符串时间转换为datetime对像
    def dbTime(self,humanTime):
        return datetime.strptime(humanTime,'%Y-%m-%d %H:%M')

    def compareTime(self,start,end):
        delta=end-start
        return delta.days#返回相差的日期

    def filterByTime(self,timeitem,start,end):
        result=Score_items.query.filter(timeitem.between(start,end)).all()
        return result

class Engine(object):
    """搜索引擎，从数据库中按需取得数据并进行包装"""
    def getUserlist_byGrade(self,grade):
        users=User.query.filter(User.grade==grade).all()
        userlist=[]
        for user in users:
            userlist.append(user)
        return userlist

    def getUserScoreitems(self,campID,timeitem,start,end):
        "返回符合条件的全部加分条目 return as a list contains all Score_items objects"
        user=User.query.filter(User.campID==campID).first()
        print user
        if start==None or end==None:
            print "@@"
            result=Score_items.query.filter(db.and_(Score_items.status==1,Score_items.user_id==user.id)).all()
        else:
            result=Score_items.query.filter(db.and_(timeitem.between(start,end),Score_items.status==1,Score_items.user_id==user.id)).all()
        # print result
        return result


    def getUserDetail(self,user,start_time=None,end_time=None,is_jsonify=True):
        userDetailDict={}
        print "getUserDetail",start_time,end_time

        items=self.getUserScoreitems(user.campID,Score_items.applytime,start_time,end_time)
        print items
        userDetailDict={
                     "name" : user.name,
                    "campID" : user.campID,
                    "grade" : user.grade,
                    "sum" : self.getSum(items),
                    "items":[]#User.scoreInfo4SomeOne(user.campID,is_jsonify=False)["items"]
        }
        for item in items:
            userDetailDict["items"].append(User.getItemInfo(item))


        if is_jsonify:
            return  jsonify(userDetailDict)
        else:
            return userDetailDict


        # def scoreInfo4SomeOne(cls,campID,is_jsonify=True,get_all=True):
        # """get someone's score_items by campID,return as json or dict,
        #     scoreInfo4SomeOne["items"] contains all the info about the score_items
        #     as a list
        # """
        # scoreInfoDict={
        # "campID":campID,
        # "items":[]
        # }
        # user=User.get_user(campID)
        # if user and user.role==ROLE_USER:
        #     items=user.score_items.all()
        #     for item in items:
        #         scoreInfoDict["items"].append(cls.getItemInfo(item))
        #     has_reslut=True
        # else:
        #     has_reslut=False
        # if  has_reslut and is_jsonify :
        #     return jsonify(scoreInfoDict)
        # elif has_reslut:
        #     return scoreInfoDict
        # else:
        #     return "No user found"



    def getSum(self,Scoreitems):
        "根据加分条目计算总分"
        total=0.0
        for Scoreitem in Scoreitems:
            total+=Scoreitem.add
        return total

    def getUserSummary(self,user,start_time=None,end_time=None,is_jsonify=True):#getUserSummary
        # user = User.get_user(campID)
        userSummaryDict={}

        Scoreitems=self.getUserScoreitems(user.campID,Score_items.applytime,Now-timedelta(days=1),Now)

        userSummaryDict={
                "name" : user.name,
                "campID" : user.campID,
                "grade" : user.grade,
                "sum" : self.getSum(Scoreitems),
            }
        if is_jsonify:
            return  jsonify(userSummaryDict)
        else:
            return userSummaryDict






if __name__ == '__main__':
    engine=Engine()
    Now=datetime.today()
    userlist=engine.getUserlist_byGrade(u"2013硕")
    st=raw_input("start time : ")
    end=raw_input("end time : ")
    print userlist
    for user in userlist:
        print  user
        # Scoreitems=engine.getUserScoreitems(user.campID,Score_items.applytime,Now-timedelta(days=2),Now)
        Scoreitems=engine.getUserScoreitems(user.campID,Score_items.applytime,st,end)
        print Scoreitems
        print engine.getSum(Scoreitems)

