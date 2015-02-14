#coding:utf-8
from flask import Flask,request,jsonify
from app import db,__ExcelDir__
from models import Excelmap,User,OPEN,CLOSE
from makeExcel import MakeExcel
from SearchEngine import Engine
import datetime
# from models import User, Score_items,ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN

def _makepublic():
    _name = request.form["name"]
    _timestart=request.form["timestart"]
    _timeend=request.form["timeend"]
    _note=request.form["note"]
    _ischecked=request.form["ischecked"]
    _adminID=request.form["admin"]#as campID
    _adminName=request.form["adminNAME"]
    _time=_maketime.strftime('%Y-%m-%d %H:%M:%S')#TODO change format?
    _grade=request.form["grade"]
    _maketime=datetime.datetime.today()
    if _ischecked=="true":
        _status=OPEN
    else:
        _status=CLOSE

    #需要写进excel的info栏的内容
    excelinfo={
             "filename" : _name,
            "start" : _timestart,
            "end" : _timeend,
            "admin" : _adminName,
            "note":_note,
            "maketime":_maketime,
            "grade":_grade
            }

    engine=Engine()
    userlist=engine.getUserlist_byGrade(_grade)#得到该年级全部的學生

    if len(userlist)==0:
        return u"不存在该年级"
    maker=MakeExcel(excelinfo)#创建MakeExcel对像并初始化
    if maker.run(userlist,_timestart,_timeend):#开始创建excel文件，接收变量userlist
        filepath=__ExcelDir__+_name+"_"+_time.split(" ")[0]+"_"+_time.split(" ")[1].replace(":","_")+".xls"
        maker.saveAs(filepath)
        #把生成的excel的相关信息存放到数据库的表中
        exceldb=Excelmap(Excelname=_name,
            creater=_adminName,
            creater_time=_maketime,
            start_time=_timestart,
            end_time=_timeend,
            filepath=filepath,
            teacher=admin,
            status=_status,
            grade=_grade
            )
        db.session.add(exceldb)
        db.session.commit()
        return "true"

    else :
        return u"0条结果，无法生成公示"


