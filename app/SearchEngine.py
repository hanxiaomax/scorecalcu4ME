#coding:utf-8
from datetime import datetime,timedelta
from models import User,Score_items
from app import db



class TimeManager(object):
    """docstring for TimeManager"""

    #把datetime对像转换为字符串形式
    def strTime(self,dbTime):
        return dbTime.strftime('%Y-%H-%d')
    #把字符串时间转换为datetime对像
    def dbTime(self,humanTime):
        return datetime.strptime(humanTime,'%Y-%H-%d')

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
            userlist.append(user.campID)
        return userlist

    def getUserScoreitems(self,campID,timeitem,start,end):
        "返回符合条件的全部加分条目"
        user=User.query.filter(User.campID==campID).first()
        result=Score_items.query.filter(db.and_(timeitem.between(start,end),Score_items.status==1,Score_items.user_id==user.id)).all()
        return result

    def getSum(self,Scoreitems):
        "根据加分条目计算总分"
        total=0.0
        for Scoreitem in Scoreitems:
            total+=Scoreitem.add
        return total


if __name__ == '__main__':
    engine=Engine()
    Now=datetime.today()
    userlist=engine.getUserlist_byGrade(u"2013硕")
    print userlist
    for user in userlist:
        print  user
        Scoreitems=engine.getUserScoreitems(user,Score_items.applytime,Now-timedelta(days=1),Now)
        print Scoreitems
        print engine.getSum(Scoreitems)

