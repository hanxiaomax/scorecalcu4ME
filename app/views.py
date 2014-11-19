#coding:utf-8
from flask import (render_template,flash,redirect,session,url_for,request,g,request,jsonify)
from flask.ext.login import (
    login_user, logout_user, current_user, login_required)

from models import User, ROLE_USER, ROLE_ADMIN
from login import LoginForm
from app import appME, db, lm

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

    return render_template(
            "user.html",
            user=user,
            user_id=user_id)


# @appME.route('/profile/student_<int:user_id>', methods=["POST", "GET"])
# @login_required
# def users_profile(user_id):
#     user = current_user
#     if not user:
#         redirect("/login/")
#     return render_template(
#             "user_profile.html",
#             user=user,
#             user_id=user_id)




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

# @appME.route('/download/', methods=["GET"])
# def download(admin_id):
#     return render_template("download.html",admin_id=admin_id)




@appME.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))


@appME.route('/_search')
def add_numbers():
    from app import myget
    return myget.mysum()
