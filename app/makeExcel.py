#coding:utf-8
from xlwt import Workbook, easyxf
from app import db,appME,__StaticDir__
from models import User, Score_items,ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN


class MakeExcel(object):
    def __init__(self,excelinfo=None):
        self.workbook = Workbook()
        self.sheet = self.workbook.add_sheet(u'公示信息')
        _tableTitle=[u"学号",u"姓名",u"年级",u"总分"]
        #设置info栏的字体
        # (<element>:(<attribute> <value>,)+;)+

        xls_title =easyxf(
            'font: name Arial,height 400,colour black;'
            'pattern: pattern solid, fore_colour pale_blue;'
            'alignment: horizontal center;'
            )
        xls_info=easyxf(
            'font: name Arial,height 300,colour black;'
            'pattern: pattern solid, fore_colour white;'
            'alignment: horizontal center;'
            'borders:top medium,bottom medium,left medium,right medium;'
            )

        _excelinfo=[excelinfo["filename"],excelinfo["start"],excelinfo["end"],excelinfo["admin"],excelinfo["note"],excelinfo["maketime"],excelinfo["grade"]]
        self.sheet.write_merge(0,2,0,10,excelinfo["filename"], xls_title)
        self.sheet.write_merge(3,4,2,10,excelinfo["admin"],xls_info)
        self.sheet.write_merge(3,4,0,1,u"创建者：",xls_info)
        self.sheet.write_merge(5,6,2,10,excelinfo["grade"],xls_info)
        self.sheet.write_merge(5,6,0,1,u"公示年级：",xls_info)
        self.sheet.write_merge(7,8,2,10,excelinfo["maketime"],xls_info)
        self.sheet.write_merge(7,8,0,1,u"创建时间：",xls_info)
        self.sheet.write_merge(9,10,2,10,excelinfo["note"],xls_info)
        self.sheet.write_merge(9,10,0,1,u"备注：",xls_info)




        for i in range(len(_tableTitle)):#Make table title
            self.sheet.write(11,i,_tableTitle[i])
        #TODO:make title

    def _writerow(self,rowNo,infobuf):
        """
        @para:rowNo(write in row nomber x)
        @para:infobuf(a dict contains someone's brief info)
        """
        _info=[infobuf["name"],infobuf["campID"],infobuf["grade"],float(infobuf["sum"])]
        for i in range(len(_info)):
            self.sheet.write(rowNo,i,_info[i])


    def _getinfobuf(self,campID):
        userInfoDict=User.userInfo(campID,is_jsonify=False,brief=True)
        return userInfoDict#return as unicode,so do not need decode in write() function




    def saveAs(self,filename):
        self.workbook.save(filename)

    def run(self,userdic):
        i=11
        for user in userdic:
            i+=1
            self._writerow(i,self._getinfobuf(user))





if __name__ == '__main__':
    maker=MakeExcel()
    maker._writerow(10,maker._getinfobuf("130280"))
    maker.saveAs(__StaticDir__+"/1.xls")



