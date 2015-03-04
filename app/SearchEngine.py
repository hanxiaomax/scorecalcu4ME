#coding:utf-8
from datetime import datetime,timedelta
from models import User,Score_items,Grade,STATUS_YES
from app import db
from flask import jsonify


class TimeManager(object):
    """与申请时间相关的一些函数封装"""

    #把datetime对像转换为字符串形式
    def strTime(self,dbTime):
        return dbTime.strftime('%Y-%m-%d %H:%M')
    #把字符串时间转换为datetime对像
    def dbTime(self,humanTime):
        return datetime.strptime(humanTime,'%Y-%m-%d')

    def filterByTime(self,time_st,time_ed,start,end):
        result=Score_items.query.filter(time_st,time_ed.between(start,end)).all()
        return result

class Engine(object):
    """搜索引擎，从数据库中按需取得数据并进行包装"""
    def __init__(self):
        self.tm=TimeManager()

    def getUserlist_byGrade(self,grade):
        """取得某个年级全部用户列表"""
        users=User.query.filter(User.grade==grade).all()
        userlist=[user for user in users]
        return userlist

    def getUserScoreitems(self,campID,time_st,time_ed,start,end):
        """返回符合条件的全部加分条目
        args:
            campID:一卡通号
            time_st
            time_ed

        """

        user=User.query.filter(User.campID==campID).first()

        if start==None or end==None:
            result=Score_items.query.filter(Score_items.user_id==user.id).all()
        else:
            #单纯求时间差，是可以用字符串的，但是如果要使用timedelta则必须要转换成datetime类型
            result=Score_items.query.filter(db.and_(time_st.between(self.tm.dbTime(start)-timedelta(days = 1),self.tm.dbTime(end)),
                                                    time_ed.between(self.tm.dbTime(start)-timedelta(days = 1),self.tm.dbTime(end)),
                                                    Score_items.user_id==user.id)).all()
        # print "start",self.tm.dbTime(start)-timedelta(days = 1)
        # print "end",self.tm.dbTime(end)-timedelta(days = 1)
        return result



    def getUserDetail(self,user,start_time=None,end_time=None,is_jsonify=True):
        """
        获取用户的具体信息
        args：
            user:用户（对象）
            start_time:统计区间起始时间
            end_time：统计区间截止时间
            is_jsonify：是否json化

        """
        if user:
            userDetailDict={}
            items=self.getUserScoreitems(user.campID,Score_items.time_st,
                                                    Score_items.time_ed,
                                                    start_time,end_time)

            userDetailDict={
                         "name" : user.name,
                        "campID" : user.campID,
                        "studentID":user.studentID,
                        "grade" : user.grade,
                        "sum" : self.getSum(items),
                        "items":[Score_items.getItemInfo(item) for item in items]#存放查询得到的全部加分项
            }


            return jsonify(userDetailDict) if is_jsonify else userDetailDict
        else:
            return u"无法找到"

    def _getcatasum(self):
        pass

    def getUserDetail_with_cata(self,user,start_time=None,end_time=None,is_jsonify=True):
        if user:
            userDetailDict={}
            items=self.getUserScoreitems(user.campID,Score_items.time_st,
                                                    Score_items.time_ed,
                                                    start_time,end_time)
            print items
            userDetailDict={
                         "name" : user.name,
                        "campID" : user.campID,
                        "studentID":user.studentID,
                        "grade" : user.grade,
                        "sum" : self.getSum(items),
                        "cata_sum":[],
                        "items":[Score_items.getItemInfo(item) for item in items]#存放查询得到的全部加分项
            }


            return jsonify(userDetailDict) if is_jsonify else userDetailDict
        else:
            return u"无法找到"



    def getUserSummary(self,user,start_time=None,end_time=None,is_jsonify=True):
        """
        获取用户的统计概况（不包括具体加分项目）
        args：
            user:用户（对象）
            start_time:统计区间起始时间
            end_time：统计区间截止时间
            is_jsonify：是否json化
        """
        if user:
            userSummaryDict={}
            Scoreitems=self.getUserScoreitems(user.campID,Score_items.time_st,Score_items.time_ed,start_time,end_time)

            userSummaryDict={
                    "id":user.id,
                    "studentID":user.studentID,
                    "name" : user.name,
                    "campID" : user.campID,
                    "grade" : user.grade,
                    "sum" : self.getSum(Scoreitems),
                }
            return jsonify(userSummaryDict) if is_jsonify else userSummaryDict
        else:
            return u"无法找到"



    def getSum(self,Scoreitems):
        "根据加分条目计算总分"
        total=0.0
        for Scoreitem in Scoreitems:
            if Scoreitem.status==STATUS_YES:#仅计算已加分数
                total+=Scoreitem.add
        return total

    def getGradeSumary(self,grade,start_time=None,end_time=None,is_jsonify=True):
        """
        获取某个年级的统计信息
        args：
            grade:年级
            start_time:统计区间起始时间
            end_time：统计区间截止时间
            is_jsonify：是否json化

        """
        userlist=self.getUserlist_byGrade(grade)
        if len(userlist)>0 :
            GradeSumaryDict={
            "grade":grade,
            "GradeSumary":[]
            }
            for user in userlist:
                u=self.getUserSummary(user,start_time,end_time,False)
                GradeSumaryDict["GradeSumary"].append(u)

            return jsonify(GradeSumaryDict) if is_jsonify else GradeSumaryDict
        else:
            return "无法找到"


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

    def getPassword(self,campID):
        u=User.get_user(campID)
        return u.password



if __name__ == '__main__':
    e=Engine()

    print e.getUserDetail_with_cata(User.get_user("000130280"),is_jsonify=False)
