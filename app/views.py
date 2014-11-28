#coding:utf-8
from flask import (render_template,flash,redirect,session,url_for,request,session,request,jsonify,send_from_directory)
from flask.ext.login import (
    login_user, logout_user, current_user, login_required)

from models import User, ROLE_USER, ROLE_ADMIN
from login import LoginForm
from app import appME, db, lm,getmyscore,saveapply,getreview
from werkzeug import secure_filename,SharedDataMiddleware
import os



@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in appME.config['ALLOWED_EXTENSIONS']



#mapping from url / and /index to this function

@appME.route('/index/') #/index will be redirect to /index/
#@login_required
def index():
    user={'nickname':'Miguel'}
    form = LoginForm()
    return render_template('index.html', title=u'HOME', user=user,form=form)

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




@appME.route('/student_<int:user_id>', methods=["POST", "GET"])
@login_required
def users(user_id):
    user = User.query.filter(User.campID == user_id).first()
    if not user:
        redirect("/login/")

    if request.method == 'POST':#利用flask框架自身的文件上传功能
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(appME.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template(
            "user.html",
            user=user,
            user_id=user_id)


@appME.route('/review/admin_<int:admin_id>', methods=["POST", "GET"])
@login_required
def admins_review(admin_id):
    admin = User.query.filter(User.campID == admin_id).first()
    if not admin:
        flash("The user is not exist.")
        redirect("/login/")
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

@appME.route('/edit/admin_<int:admin_id>', methods=["POST", "GET"])
@login_required
def admins_edit(admin_id):
    admin = User.query.filter(User.campID == admin_id).first()
    if not admin:
        flash("The user is not exist.")
        redirect("/login/")
    return render_template(
            "admin_edit.html",
            user=admin,
            admin_id=admin_id)

@appME.route('/download/', methods=["GET"])
def download():
    return render_template("download.html")




@appME.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))



@appME.route('/_getMyScore',methods=["POST", "GET"])
def _getMyScore():
    #0 :delete
    #1 :getscore
    opt=request.args.get('opt',type=int)

    if(opt==1) :
        return getmyscore._getmyscore()
    elif(opt==0):
        #if we delete an apply we will delete but not delete its 'filepath',here fixed the bug
        if session.has_key('filepath'):
            session.pop('filepath')
            return getmyscore._deleteapply(True)
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
    return send_from_directory(appME.config['UPLOAD_FOLDER'],
                               filename)


@appME.route('/_uploader',methods=["POST", "GET"])
def test():
    if request.method == 'POST':
        #campID=request.form['campID'] #get campID while uploading file
        #print request.form['filename']
        save_files()
        return 'Uploaded'


def save_file(filestorage):
    "Save a Werkzeug file storage object to the upload folder."
    filename = secure_filename(filestorage.filename)
    filepath = os.path.join(appME.config['UPLOAD_FOLDER'], filename)#path with filename
    session['filepath']=filepath
    filestorage.save(filepath)



def save_files(request=request):
    "Save all files in a request to the app's upload folder."
    for _, filestorage in request.files.iteritems():
        # Workaround: larger uploads cause a dummy file named '<fdopen>'.
        # See the Flask mailing list for more information.
        if filestorage.filename not in (None, 'fdopen', '<fdopen>'):
            save_file(filestorage)

