#coding:utf-8
from flask import (render_template,flash,redirect,session,url_for,request,session,request,jsonify,send_from_directory,g)
from flask.ext.login import (
    login_user, logout_user, current_user, login_required)

from models import User,Score_items, ROLE_USER, ROLE_ADMIN
from login import LoginForm
from app import appME, db, lm,getmyscore,saveapply,getreview
from werkzeug import secure_filename,SharedDataMiddleware
import os
import json
import uuid
basedir=os.path.abspath(os.path.dirname(__file__))
#TODO:maybe save user in g? so we dont need to query all the time?

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@appME.route('/',methods=['GET','POST'])
@appME.route('/login/',methods=['GET','POST'])
#make this view function accepts GET and POST requests
def login():
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
    #everytime this page refresh it means application has been submited ,
    #So clean the filepath because the next apply may not need to upload a pic.
    #In that case the filepath wont be update automatically
    if session.has_key('filepath'):
        session.pop('filepath')
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
            user=admin,
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

    if(opt==1) :
        return getmyscore._getmyscore()
    elif(opt==0):
        #if we delete an apply we will delete but not delete its 'filepath',here fixed the bug
        # if session.has_key('filepath'):
        #     session.pop('filepath')
        #     return getmyscore._deleteapply()
        #Moved to _deleteapply()
        return getmyscore._deleteapply()
    else:
        return getmyscore._getTotal()



@appME.route('/_sublimtApply',methods=["POST", "GET"])
def _sublimtApply():
    # in some case the user dont need to upload the pic,so we dont have Key:filepath in session
    if session.has_key('filepath'):
        print session['filepath']
        return saveapply._saveapply(session['filepath'])
    else:
        print "######"
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
    campID=request.args.get('campID',type=str)
    return User.userInfo(campID)


def save_file(filestorage):
    "Save a Werkzeug file storage object to the upload folder."
    filename = os.path.splitext(secure_filename(filestorage.filename))[0]+str(uuid.uuid1())+".jpg"
    #get filename without ext and append uuid to it to make unique file name
    filepath = os.path.join(appME.config['UPLOAD_FOLDER'], filename)#path with filename
    session['filepath']=filepath#save current filepath in session
    print "###"+session['filepath']
    filestorage.save(filepath)


def save_files(request=request):
    "Save all files in a request to the app's upload folder."
    for _, filestorage in request.files.iteritems():
        # Workaround: larger uploads cause a dummy file named '<fdopen>'.
        # See the Flask mailing list for more information.
        if filestorage.filename not in (None, 'fdopen', '<fdopen>'):
            save_file(filestorage)

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
        return "Flase"


@appME.route('/test',methods=["POST", "GET"])
def test():
    return render_template("test.html")



