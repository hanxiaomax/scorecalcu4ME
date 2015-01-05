#coding:utf-8
from flask import Flask,request,jsonify
from app import db,__ExcelDir__
from models import Excelmap,User
from makeExcel import MakeExcel
import datetime
# from models import User, Score_items,ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN

def _makepublic():
    _name=request.form["name"]
    _timestart=request.form["timestart"]
    _timeend=request.form["timeend"]
    _note=request.form["note"]
    _bischecked=request.form["bischecked"]
    _adminID=request.form["admin"]#as campID
    _adminName=request.form["adminNAME"]
    _maketime=datetime.datetime.today()
    _time=_maketime.strftime('%Y-%m-%d %H:%M:%S')
    admin=User.query.filter(User.campID == _adminID).first()
    excelinfo={
             "filename" : _name,
            "start" : _note,
            "end" : _bischecked,
            "admin" : _adminName,
            "note":_note,
            "maketime":_maketime
            }
    maker=MakeExcel(excelinfo)
    maker._writerow(12,maker._getinfobuf("130280"))
    filepath=__ExcelDir__+_name+"_"+_time.split(" ")[0]+".xls"

    maker.saveAs(filepath)

    exceldb=Excelmap(Excelname=_name,
        creater=_adminName,
        creater_time=_maketime,
        start_time=_timestart,
        end_time=_timeend,
        filepath=filepath,
        teacher=admin
        )
    db.session.add(exceldb)
    db.session.commit()


    return " "


# def _getlist():
#     excellist=Excelmap.getExcelLits()
#     return excellist
