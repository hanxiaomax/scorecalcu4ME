#coding:utf-8
from xlwt import Workbook, easyxf
from xlrd import open_workbook
from app import db,__Add_info__
from models import User
from SearchEngine import Engine,TimeManager
import re
import sqlalchemy.exc
#TODO:单元格长度
class MakeExcel(object):
    def __init__(self,excelinfo=None):
        self.STARTLINE=12
        engine=Engine()
        timemanager=TimeManager()
        self.workbook = Workbook()
        self.sheet = self.workbook.add_sheet(u'公示信息')
        _tableTitle=[u"一卡通",u"学号",u"姓名",u"年级",u"加分项",u"得分",u"总分"]
        #设置info栏的字体
        # (<element>:(<attribute> <value>,)+;)+

        xls_title =easyxf(
            'font: name Arial,height 400,colour black;'
            'pattern: pattern solid, fore_colour pale_blue;'
            'alignment: horizontal center,vertical center;'
            )
        xls_info=easyxf(
            'font: name Arial,height 250,colour black;'
            'pattern: pattern solid, fore_colour white;'
            'alignment: horizontal center,vertical center;'
            'borders:top medium,bottom medium,left medium,right medium;'
            )
        self.xls_detail=easyxf(
            'font: name Arial,height 250,colour black;'
            'pattern: pattern solid, fore_colour white;'
            'alignment: horizontal center,vertical center;'
            'borders:top medium,bottom medium,left medium,right medium;'
            )

        # _excelinfo=[excelinfo["filename"],excelinfo["start"],excelinfo["end"],excelinfo["admin"],excelinfo["note"],timemanager.strTime(excelinfo["maketime"]),excelinfo["grade"]]
        self.details=easyxf(
            'font: name Arial,height 250,colour black;'
            'pattern: pattern solid, fore_colour yellow;'
            'alignment: horizontal center,vertical center;'
            'borders:top medium,bottom medium,left medium,right medium;'
            )

        self.sheet.write_merge(0,1,0,4,excelinfo["filename"], xls_title)
        self.sheet.write_merge(2,3,2,4,excelinfo["admin"],xls_info)
        self.sheet.write_merge(2,3,0,1,u"创建者：",xls_info)
        self.sheet.write_merge(4,5,2,4,excelinfo["grade"],xls_info)
        self.sheet.write_merge(4,5,0,1,u"公示年级：",xls_info)
        self.sheet.write_merge(6,7,2,4,timemanager.strTime(excelinfo["maketime"]),xls_info)
        self.sheet.write_merge(6,7,0,1,u"创建时间：",xls_info)
        self.sheet.write_merge(8,9,2,4,excelinfo["start"]+u"至"+excelinfo["end"],xls_info)
        self.sheet.write_merge(8,9,0,1,u"统计区间：",xls_info)
        self.sheet.write_merge(10,11,2,4,excelinfo["note"],self.xls_detail)
        self.sheet.write_merge(10,11,0,1,u"备注：",xls_info)




        for i in range(len(_tableTitle)):#Make table title
            self.sheet.write(self.STARTLINE,i,_tableTitle[i],self.xls_detail)


    def _writeuser(self,rowNo,infobuf):
        """
        写用户总体信息
        """
        _info=[infobuf["campID"],infobuf["studentID"],infobuf["name"],infobuf["grade"],"","",float(infobuf["sum"])]
        for i in range(len(_info)):
            self.sheet.write(rowNo,i,_info[i],self.details)

    def _writedetail(self,rowNo,infobuf):
        """
        写具体得分细则
        """
        print infobuf
        _info=["","","","",infobuf["item_name"],float(infobuf["add"]),""]
        for i in range(len(_info)):
            self.sheet.write(rowNo,i,_info[i])


    def saveAs(self,filename):
        self.workbook.save(filename)

    def run(self,userlist,starttime,endtime):
        i=self.STARTLINE
        _count=0
        for user in userlist:#写用户总体信息
            i+=1
            engine=Engine()
            result=engine.getUserDetail(user,start_time=starttime,end_time=endtime,is_jsonify=False)
            if result is not None:
                _count+=1#增加一条记录
            self._writeuser(i,result)
            for s in result["items"]:#写具体得分细则
                i+=1
                self._writedetail(i,s)
        if _count>0:
            return True #至少有一个条目
        else:
            return False #没有任何条目


class ImportFromXls(object):
    """处理用以导入学生信息的Excel"""
    def __init__(self,filename):
        self.wb=open_workbook(filename)
        self.sheet=self.wb.sheet_by_index(0)
        self.first_col=[u'一卡通号',u'学号',u'姓名',u'年级',u'基础分']


    """"检查excel格式的合法性"""
    def isValid(self):
        for index,col in enumerate(self.sheet.row(0)):
            print col.value,self.first_col[index]
            if col.value != self.first_col[index]:
                return False
        return True


    def Read2DB(self):
        campID_not_unique=[]
        unknown=successful=num=0
        for row in range(1,self.sheet.nrows):
            stu=[col.value for col in self.sheet.row(row)]
            u=User(campID=str(stu[0]),#一卡通号
                studentID=str(stu[1]),#学号
                name=stu[2],#姓名
                grade=stu[3],#年级
                password=str(stu[0]),#密码
                role=0,score=float(stu[4])#基础分
                )
            num+=1
            try:
                db.session.add(u)
                db.session.flush()
                successful+=1
            except sqlalchemy.exc.IntegrityError :#捕获异常：学号不唯一
                db.session.rollback()#此处必须rollback()
                campID_not_unique.append(u)

            except :
                unknown+=1
                print "unknow error"



        try:
            db.session.commit()
        except:
            print "unknow error"
        return campID_not_unique,num,successful,unknown








if __name__ == '__main__':
    x=ImportFromXls(__Add_info__+"1.xlsx")
    if x.isValid():
        campID_not_unique,num,successful,unknown=x.Read2DB()

        result=u"读取"+str(num)+u"条记录\n------\n"\
        +u"成功\t\t"+str(successful)+u" 条\n------\n"\
        +u"失败(学号重复)\t"+str(len(campID_not_unique))+u" 条\n------\n"\
        +u"未知错误\t"+str(unknown)+u" 条\n------"

        print result
        if len(campID_not_unique) != 0 :
            print u"失败条目的学号为：" ,
            l=[u.campID for u in campID_not_unique]
            print l
    else:
        print "the sheet is invalid"






