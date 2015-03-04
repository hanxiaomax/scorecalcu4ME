#coding:utf-8
from xlwt import Workbook, easyxf
from xlrd import open_workbook
from app import db,__Add_info__,__ExcelDir__
from models import User
from SearchEngine import Engine,TimeManager
import re
import sqlalchemy.exc
#TODO:单元格长度
class MakeExcel(object):
    def __init__(self,excelinfo=None):
        self.STARTLINE=1
        engine=Engine()
        timemanager=TimeManager()
        self.workbook = Workbook()
        self.sheet = self.workbook.add_sheet(u'公示信息',cell_overwrite_ok=False)
        self.inforsheet=self.workbook.add_sheet(u'文档信息',cell_overwrite_ok=False)

        _tableTitle=[u"一卡通",u"学号",u"姓名",u"明细",u"说明",u"得分",u"班级年级工作",u"院级社团",u"校级社团",u"个人荣誉",u"集体荣誉",u"集体活动",u"其他",u"总分"]

        #设置列宽（固定宽度）
        self.sheet.col(0).width=4000
        self.sheet.col(1).width=4000
        self.sheet.col(2).width=3000
        self.sheet.col(3).width=10000
        self.sheet.col(4).width=10000
        self.sheet.col(5).width=2000

        self.sheet.col(6).width=4000
        self.sheet.col(7).width=3000
        self.sheet.col(8).width=3000
        self.sheet.col(9).width=3000
        self.sheet.col(10).width=3000
        self.sheet.col(11).width=3000
        self.sheet.col(12).width=3000

        self.sheet.col(13).width=2000


        #定义info栏的字体
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

        self.sumary=easyxf(
            'font: name Arial,height 250,colour black;'
            'pattern: pattern solid, fore_colour white;'
            'alignment: horizontal center,vertical center;'
            'borders:top medium,bottom medium,left medium,right medium;'
            )
        self.details=easyxf(
            'font: name Arial,height 250,colour black;'
            'pattern: pattern solid, fore_colour yellow;'
            'alignment: horizontal center,vertical center;'
            'borders:top medium,bottom medium,left medium,right medium,bottom_colour violet;'

            )



        self.inforsheet.write_merge(0,1,0,6,excelinfo["filename"], xls_title)
        self.inforsheet.write_merge(2,3,2,6,excelinfo["admin"],xls_info)
        self.inforsheet.write_merge(2,3,0,1,u"创建者：",xls_info)
        self.inforsheet.write_merge(4,5,2,6,excelinfo["grade"],xls_info)
        self.inforsheet.write_merge(4,5,0,1,u"公示年级：",xls_info)
        self.inforsheet.write_merge(6,7,2,6,timemanager.strTime(excelinfo["maketime"]),xls_info)
        self.inforsheet.write_merge(6,7,0,1,u"创建时间：",xls_info)
        self.inforsheet.write_merge(8,9,2,6,excelinfo["start"]+u"至"+excelinfo["end"],xls_info)
        self.inforsheet.write_merge(8,9,0,1,u"统计区间：",xls_info)
        self.inforsheet.write_merge(10,11,2,6,excelinfo["note"],self.xls_detail)
        self.inforsheet.write_merge(10,11,0,1,u"备注：",xls_info)


        for i in range(len(_tableTitle)):#Make table title
            self.sheet.write(0,i,_tableTitle[i],self.xls_detail)



    def _writeuser(self,rowNo,infobuf,lines):
        """
        写用户总体信息
        """
        _info=[infobuf["campID"],infobuf["studentID"],infobuf["name"],u"无",u"无",u"0",infobuf["cata_sum"][0][1],infobuf["cata_sum"][1][1],infobuf["cata_sum"][2][1],infobuf["cata_sum"][3][1],infobuf["cata_sum"][4][1],infobuf["cata_sum"][5][1],infobuf["cata_sum"][6][1],float(infobuf["sum"])]
        #infobuf["cata_sum"][2][1] 为(u"院级社团",catC)里面的catC
        if lines==0:#如果无加分
            for i in range(len(_info)):
                self.sheet.write_merge(rowNo,rowNo+lines,i,i,_info[i],self.sumary)
            return lines+1
        else:
            for i in range(len(_info)):
                if i not in [3,4,5]:#明细,分值留空
                    self.sheet.write_merge(rowNo,rowNo+lines-1,i,i,_info[i],self.sumary)
            return lines

    def _writedetail(self,rowNo,items,lines):
        """
        写具体得分细则
        """
        i=0
        for item in items:
            _info=[item["item_name"],item["note"],item["add"]]
            for s in range(len(_info)):
                self.sheet.write(rowNo+i,3+s,_info[s],self.details)
            i+=1


    def saveAs(self,filename):
        self.workbook.save(filename)

    def run(self,userlist,starttime,endtime):
        try:
            i=self.STARTLINE
            _count=0
            for user in userlist:#写用户总体信息
                engine=Engine()
                #result=engine.getUserDetail(user,start_time=starttime,end_time=endtime,is_jsonify=False)
                result=engine.getUserDetail_with_cata(user,start_time=starttime,end_time=endtime,is_jsonify=False)
                lines=len(result["items"])
                if result is not None:
                    _count+=1#增加一条记录
                self._writedetail(i,result["items"],lines)
                #self._writeCataSum(i,result["cata_sum"],lines)
                i+=self._writeuser(i,result,lines)
            if _count>0:
                print "111"
                return True #至少有一个条目
            else:
                return False #没有任何条目

        except Exception, e:
            print e
            raise e



class ImportFromXls(object):
    """处理用以导入学生信息的Excel"""
    def __init__(self,filename):
        self.wb=open_workbook(filename)
        self.sheet=self.wb.sheet_by_index(0)
        self.first_col=[u'一卡通号',u'学号',u'姓名',u'年级',u'基础分']


    """"检查excel格式的合法性"""
    def isValid(self):
        for index,col in enumerate(self.sheet.row(0)):
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
    excelinfo={
             "filename" : "_name",
            "start" : "_timestart",
            "end" : "_timeend",
            "admin" : "_adminName",
            "note":"_note",
            "maketime":"_maketime",
            "grade":"_grade"
            }
    engine=Engine()
    userlist=engine.getUserlist_byGrade(u"本2013")#得到该年级全部的學生
    maker=MakeExcel(excelinfo)#创建MakeExcel对像并初始化
    if maker.run(userlist,"2015-03-01","2015-03-30"):#开始创建excel文件，接收变量userlist
        filepath=__ExcelDir__+"_name"+"_"+".xls"
        maker.saveAs(filepath)



    # x=ImportFromXls(__Add_info__+"1.xlsx")
    # if x.isValid():
    #     campID_not_unique,num,successful,unknown=x.Read2DB()

    #     result=u"读取"+str(num)+u"条记录\n------\n"\
    #     +u"成功\t\t"+str(successful)+u" 条\n------\n"\
    #     +u"失败(学号重复)\t"+str(len(campID_not_unique))+u" 条\n------\n"\
    #     +u"未知错误\t"+str(unknown)+u" 条\n------"

    #     print result
    #     if len(campID_not_unique) != 0 :
    #         print u"失败条目的学号为：" ,
    #         l=[u.campID for u in campID_not_unique]
    #         print l
    # else:
    #     print "the sheet is invalid"






