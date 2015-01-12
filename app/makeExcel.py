#coding:utf-8
from xlwt import Workbook, easyxf
from app import db,appME,__StaticDir__
from models import User, Score_items,ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN
from SearchEngine import Engine,TimeManager
#TODO:单元格长度
class MakeExcel(object):
    def __init__(self,excelinfo=None):
        self.STARTLINE=12
        engine=Engine()
        timemanager=TimeManager()
        self.workbook = Workbook()
        self.sheet = self.workbook.add_sheet(u'公示信息')
        _tableTitle=[u"学号",u"姓名",u"年级",u"总分",u"备注"]
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


        self.sheet.write_merge(0,1,0,4,excelinfo["filename"], xls_title)
        self.sheet.write_merge(2,3,2,4,excelinfo["admin"],xls_info)
        self.sheet.write_merge(2,3,0,1,u"创建者：",xls_info)
        self.sheet.write_merge(4,5,2,4,excelinfo["grade"],xls_info)
        self.sheet.write_merge(4,5,0,1,u"公示年级：",xls_info)
        self.sheet.write_merge(6,7,2,4,timemanager.strTime(excelinfo["maketime"]),xls_info)
        self.sheet.write_merge(6,7,0,1,u"创建时间：",xls_info)
        self.sheet.write_merge(8,9,2,4,excelinfo["start"]+u"至"+excelinfo["end"],xls_info)
        self.sheet.write_merge(8,9,0,1,u"公示区间：",xls_info)
        self.sheet.write_merge(10,11,2,4,excelinfo["note"],self.xls_detail)
        self.sheet.write_merge(10,11,0,1,u"备注：",xls_info)




        for i in range(len(_tableTitle)):#Make table title
            self.sheet.write(self.STARTLINE,i,_tableTitle[i],self.xls_detail)


    def _writerow(self,rowNo,infobuf):
        """
        @para:rowNo(write in row nomber x)
        @para:infobuf(a dict contains someone's brief info)
        """
        _info=[infobuf["campID"],infobuf["name"],infobuf["grade"],float(infobuf["sum"])]
        for i in range(len(_info)):
            self.sheet.write(rowNo,i,_info[i])


    def _getinfobuf(self,campID):
        # userInfoDict=engine.getUserSummary(is_jsonify=False)

        # return userInfoDict#return as unicode,so do not need decode in write() function
        pass




    def saveAs(self,filename):
        self.workbook.save(filename)

    def run(self,userlist,starttime,endtime):
        i=self.STARTLINE
        _count=0
        for user in userlist:
            i+=1

            engine=Engine()
            result=engine.getUserSummary(user,starttime,endtime,is_jsonify=False)
            print result
            if result is not None:
                _count+=1#增加一条记录
            self._writerow(i,result)
        if _count>0:
            return True #至少有一个条目
        else:
            return False #没有任何条目





if __name__ == '__main__':
    maker=MakeExcel()
    maker._writerow(10,maker._getinfobuf("130280"))
    maker.saveAs(__StaticDir__+"/1.xls")



