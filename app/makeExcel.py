#coding:utf-8
import xlwt
from app import db,appME,__StaticDir__
from models import User, Score_items,ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN


class MakeExcel(object):
    def __init__(self):
        self.workbook = xlwt.Workbook()
        self.sheet = self.workbook.add_sheet(u'公示信息')
        _tableTitle=[u"学号",u"姓名",u"年级",u"总分"]
        for i in range(len(_tableTitle)):#Make table title
            self.sheet.write(0,i,_tableTitle[i])
        #TODO:make title

    def _writerow(self,rowNo,infobuf):
        """
        @para:rowNo(write in row nomber x)
        @para:infobuf(a dict contains someone's brief info)
        """
        _info=[infobuf["name"],infobuf["campID"],infobuf["grade"],infobuf["sum"]]
        for i in range(len(_info)):
            self.sheet.write(rowNo,i,_info[i])


    def _getinfobuf(self,campID):
        userInfoDict=User.userInfo(campID,is_jsonify=False,brief=True)
        print userInfoDict
        return userInfoDict#return as unicode,so do not need decode in write() function


    def saveAs(self,filename):
        self.workbook.save(filename)



maker=MakeExcel()
maker._writerow(1,maker._getinfobuf("130280"))
maker.saveAs(__StaticDir__+"/1.xls")
print __StaticDir__


