#coding:utf-8
from flask import Flask,request,jsonify
from app import db,__ExcelDir__
from models import Excelmap,User,OPEN,CLOSE
from makeExcel import MakeExcel
from SearchEngine import Engine
import datetime
# from models import User, Score_items,ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN

def _makepublic():
    _name=request.form["name"]
    _timestart=request.form["timestart"]
    _timeend=request.form["timeend"]
    _note=request.form["note"]
    _ischecked=request.form["ischecked"]
    _adminID=request.form["admin"]#as campID
    _adminName=request.form["adminNAME"]
    _maketime=datetime.datetime.today()
    _time=_maketime.strftime('%Y-%m-%d %H:%M:%S')#TODO change format?
    _grade=request.form["grade"]
    admin=User.query.filter(User.campID == _adminID).first()


    if _ischecked=="true":
        _status=OPEN
    else:
        _status=CLOSE

    #需要写进excel的info栏的内容
    excelinfo={
             "filename" : _name,
            "start" : _note,
            "end" : _timeend,
            "admin" : _adminName,
            "note":_note,
            "maketime":_maketime,
            "grade":_grade
            }

    engine=Engine()
    userlist=engine.getUserlist_byGrade(_grade)#得到该年级全部人的学号

    maker=MakeExcel(excelinfo)#创建MakeExcel对像并初始化
    maker.run(userlist)#开始创建excel文件，接收变量userlist

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
        status=_status
        )
    db.session.add(exceldb)
    db.session.commit()


    return " "

