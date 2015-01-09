#coding:utf-8
from datetime import datetime,timedelta
from models import User,Score_items,STATUS_YES
from app import db
from flask import jsonify


class TimeManager(object):
    """docstring for TimeManager"""

    #把datetime对像转换为字符串形式
    def strTime(self,dbTime):
        return dbTime.strftime('%Y-%m-%d %H:%M')
    #把字符串时间转换为datetime对像
    def dbTime(self,humanTime):
        return datetime.strptime(humanTime,'%Y-%m-%d')

    def compareTime(self,start,end):
        delta=end-start
        return delta.days#返回相差的日期

    def filterByTime(self,timeitem,start,end):
        result=Score_items.query.filter(timeitem.between(start,end)).all()
        return result

class Engine(object):
    """搜索引擎，从数据库中按需取得数据并进行包装"""
    def __init__(self):
        self.tm=TimeManager()

    def getUserlist_byGrade(self,grade):
        users=User.query.filter(User.grade==grade).all()
        userlist=[]
        for user in users:
            userlist.append(user)
        return userlist

    # def _searchWithTime(self,timeitem,start,end):
    #     return Score_items.query.filter(db.and_(timeitem.between(start+timedelta(days+1),end),Score_items.status==1,Score_items.user_id==user.id)).all()

    def getUserScoreitems(self,campID,timeitem,start,end):
        "返回符合条件的全部加分条目 return as a list contains all Score_items objects"
        user=User.query.filter(User.campID==campID).first()

        # if status==STATUS_YES:
        #     result=Score_items.query.filter(db.and_(Score_items.status==STATUS_YES,Score_items.user_id==user.id)).all()
        # elif status==STATUS_NO:
        #     result=Score_items.query.filter(db.and_(Score_items.status==STATUS_NO,Score_items.user_id==user.id)).all()
        # elif status ==STATUS_UNKNOWN:
        #     result=Score_items.query.filter(db.and_(Score_items.status==STATUS_UNKNOWN,Score_items.user_id==user.id)).all()
        # else:
        #     result=Score_items.query.filter(db.and_(Score_items.user_id==user.id)).all()


        if start==None or end==None:
            result=Score_items.query.filter(Score_items.user_id==user.id).all()
        else:
            #单纯求时间差，是可以用字符串的，但是如果要使用timedelta则必须要转换成datetime类型
            result=Score_items.query.filter(db.and_(timeitem.between(self.tm.dbTime(start),self.tm.dbTime(end)+timedelta(days=1)),Score_items.user_id==user.id)).all()
        # print result
        return result


    def getUserDetail(self,user,start_time=None,end_time=None,is_jsonify=True):
        if user:
            userDetailDict={}
            items=self.getUserScoreitems(user.campID,Score_items.applytime,start_time,end_time)

            userDetailDict={
                         "name" : user.name,
                        "campID" : user.campID,
                        "grade" : user.grade,
                        "sum" : self.getSum(items),
                        "items":[]
            }
            for item in items:
                userDetailDict["items"].append(User.getItemInfo(item))


            if is_jsonify:
                return  jsonify(userDetailDict)
            else:
                return userDetailDict
        else:
            return u"无法找到"


    def getSum(self,Scoreitems):
        "根据加分条目计算总分"
        total=0.0
        for Scoreitem in Scoreitems:
            if Scoreitem.status==STATUS_YES:#仅计算已加分数
                total+=Scoreitem.add
        return total

    def getUserSummary(self,user,start_time=None,end_time=None,is_jsonify=True):#getUserSummary
        if user:
            userSummaryDict={}

            Scoreitems=self.getUserScoreitems(user.campID,Score_items.applytime,start_time,end_time)

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
        else:
            return u"无法找到"

    def getGradeSumary(self,grade,start_time=None,end_time=None,is_jsonify=True):

        userlist=self.getUserlist_byGrade(grade)
        GradeSumaryDict={
        "grade":grade,
        "GradeSumary":[]
        }
        for user in userlist:
            u=self.getUserSummary(user,start_time,end_time,False)
            GradeSumaryDict["GradeSumary"].append(u)

        if is_jsonify:
            return  jsonify(GradeSumaryDict)
        else:
            return GradeSumaryDict







    #TODO:是否应该在获取getgradesumary函数内部调用而不是在view中？
    #在生成公示前进行全局更新，另有两处更新分别在搜索前和用户个人登陆前，只更新个人，使用_getTotal(user)函数
    def updateTotal(self):
        users=User.query.all()
        for user in users:
            _score_items=user.score_items.all()
            total=0.0
            for s in _score_items:
                if (s.status==STATUS_YES):
                    if s.add is not None:
                        total+=s.add
            user.score=total

        db.session.commit()









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

