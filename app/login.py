#coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField,BooleanField,PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    username=StringField('username',validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
#validators=[DataRequired()] only need user to input no matter what

