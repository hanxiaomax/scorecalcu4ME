#coding:utf-8
from flask import Flask,request,jsonify
from app import db,__StaticDir__
from makeExcel import MakeExcel
import datetime
# from models import User, Score_items,ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN

def _makepublic():
    _name=request.form["name"]
    _timestart=request.form["timestart"]
    _timeend=request.form["timeend"]
    _note=request.form["note"]
    _bischecked=request.form["bischecked"]
    _admin=request.form["admin"]
    _maketime=datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print _maketime.split(" ")[0]
    excelinfo={
             "filename" : _name,
            "start" : _note,
            "end" : _bischecked,
            "admin" : _admin,
            "note":_note,
            "maketime":_maketime
            }
    maker=MakeExcel(excelinfo)
    maker._writerow(12,maker._getinfobuf("130280"))
    maker.saveAs(__StaticDir__+_name+"_"+_maketime.split(" ")[0]+".xls")


    return " "
