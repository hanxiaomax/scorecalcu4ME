#coding:utf-8
#flask相关模块
from flask import (render_template,flash,redirect,session,url_for,request,request,jsonify,send_from_directory,g,escape)
from flask.ext.login import (
    login_user, logout_user, current_user, login_required)
#模型
from models import User,Score_items,Grade,Excelmap, ROLE_USER, ROLE_ADMIN
#登陆模块
from login import LoginForm
from app import appME, db, lm,getmyscore,saveapply,getreview,__StaticDir__,makepublic,__ExcelDir__
from werkzeug import secure_filename,SharedDataMiddleware
#搜索引擎模块，处理数据库查询
from SearchEngine import Engine
#excel导入模块
from makeExcel import ImportFromXls
import os
import json
import uuid
import sqlalchemy.exc
basedir=os.path.abspath(os.path.dirname(__file__))





########################页面路由########################

#登陆页面路由
@appME.route('/',methods=['GET','POST'])
@appME.route('/login/',methods=['GET','POST'])
#make this view function accepts GET and POST requests
def login():
    #print __StaticDir__
    form = LoginForm()
    if form.validate_on_submit():
        user=User.login_check(request.form.get('username'),request.form.get('password'))
        #get the username and password form the form
        if user:
            login_user(user)#login
            #go to page accoding to the role using current user's campID as the user_id
            if user.role==ROLE_USER:
                return redirect(url_for('users', user_id = current_user.campID))
            elif user.role==ROLE_ADMIN:
                return redirect(url_for('admins_review', admin_id = current_user.campID))
            else:
                return redirect("/login/")
        else:
            flash(u"用户名或密码错误")

    return render_template('login.html',
                            title=u'机械工程学院素质分管理系统',
                            form=form)


#学生申请页面路由---->user.html
@appME.route('/student_<int:user_id>', methods=["POST", "GET"])
@login_required
def users(user_id):
    #type(user_id):int
    #type(current_user.campID):unicode
    #you can only view your page!
    if user_id!=int(current_user.campID):
        return redirect("/login/")

    user = User.query.filter(User.campID == user_id).first()

    if not user:
        redirect("/login/")
    return render_template(
            "user.html",
            user=user,
            user_id=user_id)

#学生公示页面路由---->user_publicity.html
@appME.route('/publicity/student_<int:user_id>', methods=["POST", "GET"])
@login_required
def user_publicity(user_id):
    user = User.query.filter(User.campID == user_id).first()
    if not user:
        flash("The user is not exist.")
        redirect("/login/")
    return render_template(
            "user_publicity.html",
            user=user,
            user_id=user_id)


#教师审核页面路由---->admin.html
@appME.route('/review/admin_<int:admin_id>', methods=["POST", "GET"])
@login_required
def admins_review(admin_id):
    admin = User.query.filter(User.campID == admin_id).first()
    return render_template(
            "admin.html",
            user=admin,
            admin_id=admin_id)

#教师查询页面路由---->admin_search.html
@appME.route('/search/admin_<int:admin_id>', methods=["POST", "GET"])
@login_required
def admins_search(admin_id):
    admin = User.query.filter(User.campID == admin_id).first()
    if not admin:
        flash("The user is not exist.")
        redirect("/login/")
    return render_template(
            "admin_search.html",
            user=admin,
            admin_id=admin_id)

#教师公示页面路由---->admin_publicity.html
@appME.route('/publicity/admin_<int:admin_id>', methods=["POST", "GET"])
@login_required
def admins_publicity(admin_id):
    admin = User.query.filter(User.campID == admin_id).first()
    if not admin:
        flash("The user is not exist.")
        redirect("/login/")
    return render_template(
            "admin_publicity.html",
            user=admin,adminname=admin.name,
            admin_id=admin_id)

#学生更改密码页面路由
@appME.route('/changePassword_<int:user_id>/')
def changePassword(user_id):
    user = User.query.filter(User.campID == user_id).first()
    return render_template("changePassword.html",user=user)

#下载页面路由
@appME.route('/download/', methods=["GET"])
def download():
    return render_template("download.html")


#下载excel文档路由
@appME.route('/download_excel/<filename>')
def download_excel(filename):
    "download excel"

    return send_from_directory(__ExcelDir__,
                               filename)



#后台管理页面路由
@appME.route('/management/admin_<int:admin_id>', methods=["POST", "GET"])
@login_required
def management(admin_id):
    admin = User.query.filter(User.campID == admin_id).first()
    if not admin:
        flash("The user is not exist.")
        redirect("/login/")
    return render_template(
            "management.html",
            user=admin,
            admin_id=admin_id)

#教师帮助文档路由
@appME.route('/helpteacher/')
#make this view function accepts GET and POST requests
def helpteacher():
    return render_template('ReadMeTEA.html',
                            title=u'机械工程学院素质分管理系统',
                            )

#帮助文档路由
@appME.route('/help/')
def help():
    return render_template('ReadMe.html',
                            title=u'机械工程学院素质分管理系统',
                            )
#404页面路由
@appME.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404




##############################功能函数########################
#登陆
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#注销
@appME.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))




#学生页面获取表格内信息
@appME.route('/_getMyScore',methods=["POST", "GET"])
def _getMyScore():
    "getmyscore.py:scripts used by user.html"
    #0 :delete
    #1 :getscore
    opt=request.args.get('opt',type=int)
    campID = request.args.get('campID', type=str)
    user=User.get_user(campID)
    if user:
        if(opt==1) :
            return getmyscore._getmyscore(user)
        elif(opt==0):
            return getmyscore._deleteapply(user)
        else:
            return getmyscore._getTotal(user)#Update the total score (called when searching or login)
    else:
        return "user not found"


#提交申请
@appME.route('/_sublimtApply',methods=["POST", "GET"])
def _sublimtApply():
        return saveapply._saveapply()





#处理后台管理页面的操作
@appME.route('/_management',methods=["POST", "GET"])
def management_handle():
    if request.method == 'POST':
        return makepublic._makepublic()
    elif request.method == 'GET':
        if request.args.get('Delete',type=str)=='Delete':#删除某个加分项
            itemID=request.args.get('itemID',type=int)
            Score_items.delete(itemID)
            return " "
        elif request.args.get('Delete',type=str)=='DeleteStu':#删除学生
            campID=request.args.get('campID',type=str)
            User.delete(campID)
            return " "
        elif request.args.get('Edit',type=str)=='Edit':#编辑
            id=request.args.get('id',type=str)
            name=request.args.get('edit_name',type=unicode)
            campID=request.args.get('edit_campID',type=str)
            grade=request.args.get('edit_grade',type=unicode)
            # print "id:"+id
            # print "name:"+name
            # print "campID:"+campID
            # print "grade:"+grade

            return User.edit(id,campID,name,grade)


        elif request.args.get('Add',type=str)=='Add':#添加学生
            name=request.args.get('add_name',type=unicode)
            campID=request.args.get('add_campID',type=str)
            grade=request.args.get('add_grade',type=unicode)
            user=User.get_user(campID)
            if user:
                return u"学号重复"
            else :
                User.addstudent(campID,name,grade)
                return u"添加成功"

#处理公示页面的相关操作
@appME.route('/_makepublic',methods=["POST", "GET"])
def makePublic():
    if request.method == 'POST':
        return makepublic._makepublic()#生成公示信息
    elif request.method == 'GET':
        if request.args.get('Delete',type=str)=='Delete':#删除公示信息
            excelID=request.args.get('id',type=int)
            Excelmap.deleteExcel(excelID)
            return " "
        elif request.args.get('View',type=str)=='View':#查看公示信息
            excelID=request.args.get('id',type=int)
            e=Excelmap.query.filter(excelID==Excelmap.id).first()
            filename= os.path.basename(e.filepath)
            return url_for('download_excel', filename = filename)

        elif request.args.get('Changestatus',type=str)=='Changestatus':#改变公示状态
            excelID=request.args.get('id',type=int)
            e=Excelmap.query.filter(excelID==Excelmap.id).first()
            _status=request.args.get('status',type=int)
            e.status=_status
            db.session.commit()
            return str(_status)
        elif request.args.get('act',type=str)=='updateTotal':#更新总分
            engine=Engine()
            engine.updateTotal()
            return " "
        else:
            #返回excel公示列表
            return Excelmap.getExcelLits()#must be a jsonify object or it will return dict is not callable

#从excel导入文件
@appME.route('/_import_stu_from_xlsx',methods=["POST", "GET"])
def import_stu_from_xlsx():
    filename=request.args.get('excelname',type=unicode)
    filepath = os.path.join(appME.config['UPLOAD_EXCEL'], filename)#path with filename
    #TODO:检查扩展名
    x=ImportFromXls(filepath)
    if x.isValid():
        campID_not_unique,num,successful,unknown=x.Read2DB()

        result=u"读取"+str(num)+u"条记录\n------\n"\
        +u"成功\t\t"+str(successful)+u" 条\n------\n"\
        +u"失败(学号重复)\t"+str(len(campID_not_unique))+u" 条\n------\n"\
        +u"未知错误\t"+str(unknown)+u" 条\n------"

        result_dic={
        "result":result,
        "failed_list":[u.campID for u in campID_not_unique]  if len(campID_not_unique) != 0 else None
        }

        #如果有错误的campID，则收集它们，否则设置为None

        os.remove(filepath)#使用完成后删除excel文件
        return jsonify(result_dic)

    else:
        result_dic={"result":u"上传的Excel文件格式不正确"}
        os.remove(filepath)
        return jsonify(result_dic)

#更改密码
@appME.route('/_changePW',methods=["POST", "GET"])
def changePW():
    campID=request.args.get('campID',type=str)
    oldpw=request.args.get('oldpw')
    newpw=request.args.get('newpw')
    user=User.get_user(campID)
    if user.password == oldpw:
        user.password=newpw
        db.session.commit()
        return "True"
    else:
        return "False"


@appME.route('/test',methods=["POST", "GET"])
def test():
    # return render_template("123")
    return "hello world"

#保存excel格式文件
def save_excel(filestorage,filename):
    filepath = os.path.join(appME.config['UPLOAD_EXCEL'], filename)#path with filename
    filestorage.save(filepath)

#保存图片类型的文件
def save_file(filestorage,uuid):
    "Save a Werkzeug file storage object to the upload folder."
    filename=str(uuid)+".jpg"
    filepath = os.path.join(appME.config['UPLOAD_FOLDER'], filename)#path with filename
    filestorage.save(filepath)

#保存文件，文件类型为type
def save_files(type,request=request):
    for _, filestorage in request.files.iteritems():
        # Workaround: larger uploads cause a dummy file named '<fdopen>'.
        # See the Flask mailing list for more information.
        if filestorage.filename not in (None, 'fdopen', '<fdopen>'):
            if type=="excel":
                save_excel(filestorage,filestorage.filename)
            elif type=="pic":
                UUID=request.form.get("UUID")#FORM NOT ARGES
                save_file(filestorage,UUID)


#获取待审核信息
@appME.route('/_getreview',methods=["POST", "GET"])
def _getreview():
    opt2=request.args.get('opt2',type=int)
    if(opt2==0) :#reject
        return getreview._reject()
    elif(opt2==1):#accpet
        return getreview._accpet()
    else:
        return getreview._getreview()

#管理年级信息
@appME.route('/_grade_management',methods=["POST", "GET"])
def _grade_management():
    action=request.args.get('action',type=str)
    if action=="add_grade":
        grade=request.args.get('grade',type=unicode)
        if not Grade.query.filter(Grade.grade_name==grade).first():
            g=Grade(grade_name=grade)
        else:
            return u"该年级已经存在"
        try:
            db.session.add(g)
            db.session.commit()
            #重新生成grade.json文件
            generateGradeJson()
            return u"添加成功"
        # except sqlalchemy.exc.IntegrityError, e:
        #     db.session.rollback()#此处必须rollback()
        #     return u"该年级已经存在"
        except :
            return u"发生未知错误"
    elif action=="del_grade":
        grade=request.args.get('grade',type=unicode)
        g=Grade.query.filter(Grade.grade_name==grade).first()
        try:
            db.session.delete(g)
            generateGradeJson()
            db.session.commit()
            return u"删除成功"
        except :
            return u"发生未知错误"


def generateGradeJson():
    try:
        grades=[grade.grade_name for grade in Grade.query.all()]
        grade_dict={
        "grade":[grade.encode('utf-8') for grade in grades ]
        }

        with open(__StaticDir__+"grade.json",'w') as f:
            f.write(json.dumps(grade_dict))#把json格式的内容写入文件
    except:
        raise




#获取图片
@appME.route('/uploads/<filename>')
def uploaded_file(filename):
    "send picture"

    return send_from_directory(appME.config['UPLOAD_FOLDER'],
                               filename)

#处理图片上传操作
@appME.route('/_uploader',methods=["POST", "GET"])
def picuploader():
    if request.method == 'POST':
        save_files("pic")
        return 'Uploaded'

#处理excel上传操作
@appME.route('/_uploadxlsx',methods=["POST", "GET"])
def exceluploader():
    if request.method == 'POST':
        save_files("excel")
        return 'Uploaded'



#处理获取学生信息
@appME.route('/_getStuInfo',methods=["POST", "GET"])
def getStuInfo():
    engine=Engine()
    searchtype=request.args.get('searchtype',type=str)
    starttime=request.args.get('starttime',type=unicode)
    endtime=request.args.get('endtime',type=unicode)

    if  searchtype=="bycampID":
        campID=request.args.get('campID',type=str)
        user=User.get_user(campID)

        return engine.getUserDetail(user,starttime,endtime)
    elif searchtype=="bygrade":
        grade=request.args.get('grade',type=unicode)
        engine.updateTotal()#如果按年级查询，更新数据库总分
        return engine.getGradeSumary(grade,starttime,endtime)
    else:
        return u"无法找到"

