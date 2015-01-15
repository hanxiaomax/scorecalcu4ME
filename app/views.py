#coding:utf-8
from flask import (render_template,flash,redirect,session,url_for,request,request,jsonify,send_from_directory,g,escape)
from flask.ext.login import (
    login_user, logout_user, current_user, login_required)

from models import User,Score_items, ROLE_USER, ROLE_ADMIN,Excelmap
from login import LoginForm
from app import appME, db, lm,getmyscore,saveapply,getreview,__StaticDir__,makepublic,__ExcelDir__
from werkzeug import secure_filename,SharedDataMiddleware
import os
import json
import uuid
from SearchEngine import Engine
basedir=os.path.abspath(os.path.dirname(__file__))

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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

#user.html
#Dashboard for student to apply
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

#Dashboard for student to checkout the publicity
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

@appME.route('/review/admin_<int:admin_id>', methods=["POST", "GET"])
@login_required
def admins_review(admin_id):
    admin = User.query.filter(User.campID == admin_id).first()
    return render_template(
            "admin.html",
            user=admin,
            admin_id=admin_id)


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

@appME.route('/download/', methods=["GET"])
def download():
    return render_template("download.html")




@appME.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))



@appME.route('/changePassword_<int:user_id>/')
def changePassword(user_id):
    user = User.query.filter(User.campID == user_id).first()
    return render_template("changePassword.html",user=user)


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



@appME.route('/_sublimtApply',methods=["POST", "GET"])
def _sublimtApply():
        return saveapply._saveapply()



@appME.route('/_getreview',methods=["POST", "GET"])
def _getreview():
    opt2=request.args.get('opt2',type=int)
    if(opt2==0) :#reject
        return getreview._reject()
    elif(opt2==1):#accpet
        return getreview._accpet()
    else:
        return getreview._getreview()


@appME.route('/uploads/<filename>')
def uploaded_file(filename):
    "send picture"

    return send_from_directory(appME.config['UPLOAD_FOLDER'],
                               filename)


@appME.route('/_uploader',methods=["POST", "GET"])
def uploader():
    if request.method == 'POST':
        save_files()
        return 'Uploaded'

@appME.route('/_getStuInfo',methods=["POST", "GET"])
def getStuInfo():
    engine=Engine()
    searchtype=request.args.get('searchtype',type=str)
    starttime=request.args.get('starttime',type=unicode)
    endtime=request.args.get('endtime',type=unicode)
    if  searchtype=="bycampID":
        campID=request.args.get('campID',type=str)
        user=User.get_user(campID)
        # for i in engine.getUserDetail(user,starttime,endtime,False)["items"]:
        #     print i
        return engine.getUserDetail(user,starttime,endtime)
    elif searchtype=="bygrade":
        grade=request.args.get('grade',type=unicode)
        engine.updateTotal()#如果按年级查询，更新数据库总分
        return engine.getGradeSumary(grade,starttime,endtime)
    else:
        return u"无法找到"


def save_file(filestorage,uuid):
    "Save a Werkzeug file storage object to the upload folder."
    #filename = os.path.splitext(secure_filename(filestorage.filename))[0]+str(uuid.uuid1())+".jpg"
    filename=str(uuid)+".jpg"
    filepath = os.path.join(appME.config['UPLOAD_FOLDER'], filename)#path with filename
    filestorage.save(filepath)


def save_files(request=request):
    "Save all files in a request to the app's upload folder."
    UUID=request.form.get("UUID")#FORM NOT ARGES
    for _, filestorage in request.files.iteritems():
        # Workaround: larger uploads cause a dummy file named '<fdopen>'.
        # See the Flask mailing list for more information.
        if filestorage.filename not in (None, 'fdopen', '<fdopen>'):
            save_file(filestorage,UUID)

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
    return render_template("test.html")

@appME.route('/_makepublic',methods=["POST", "GET"])
def makePublic():
    if request.method == 'POST':
        return makepublic._makepublic()
    elif request.method == 'GET':
        if request.args.get('Delete',type=str)=='Delete':
            excelID=request.args.get('id',type=int)
            Excelmap.deleteExcel(excelID)
            return " "
        elif request.args.get('View',type=str)=='View':
            excelID=request.args.get('id',type=int)
            e=Excelmap.query.filter(excelID==Excelmap.id).first()
            filename= os.path.basename(e.filepath)
            return url_for('download_excel', filename = filename)

        elif request.args.get('Changestatus',type=str)=='Changestatus':
            excelID=request.args.get('id',type=int)
            e=Excelmap.query.filter(excelID==Excelmap.id).first()
            _status=request.args.get('status',type=int)
            e.status=_status
            db.session.commit()
            return str(_status)
        elif request.args.get('act',type=str)=='updateTotal':
            engine=Engine()
            engine.updateTotal()
            return " "
        else:
            return Excelmap.getExcelLits()#must be a jsonify object or it will return dict is not callable

@appME.route('/download_excel/<filename>')
def download_excel(filename):
    "download excel"

    return send_from_directory(__ExcelDir__,
                               filename)






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


@appME.route('/helpteacher/')
#make this view function accepts GET and POST requests
def helpteacher():
    return render_template('ReadMeTEA.html',
                            title=u'机械工程学院素质分管理系统',
                            )
@appME.route('/help/')
#make this view function accepts GET and POST requests
def help():
    return render_template('ReadMe.html',
                            title=u'机械工程学院素质分管理系统',
                            )

@appME.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@appME.route('/_management',methods=["POST", "GET"])
def management_handle():
    if request.method == 'POST':
        return makepublic._makepublic()
    elif request.method == 'GET':
        if request.args.get('Delete',type=str)=='Delete':
            itemID=request.args.get('itemID',type=int)
            Score_items.delete(itemID)
            return " "
        elif request.args.get('Delete',type=str)=='DeleteStu':
            campID=request.args.get('campID',type=str)
            User.delete(campID)
            return " "
        elif request.args.get('Edit',type=str)=='Edit':
            id=request.args.get('id',type=str)
            name=request.args.get('edit_name',type=unicode)
            campID=request.args.get('edit_campID',type=str)
            grade=request.args.get('edit_grade',type=unicode)
            # print "id:"+id
            # print "name:"+name
            # print "campID:"+campID
            # print "grade:"+grade

            return User.edit(id,campID,name,grade)


        elif request.args.get('Add',type=str)=='Add':
            name=request.args.get('add_name',type=unicode)
            campID=request.args.get('add_campID',type=str)
            grade=request.args.get('add_grade',type=unicode)
            user=User.get_user(campID)
            if user:
                return u"学号重复"
            else :
                User.addstudent(campID,name,grade)
                return u"添加成功"








