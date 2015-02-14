from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import os
# from SearchEngine import Engine

__StaticDir__=os.path.abspath(os.path.dirname(__file__))+"/static/"
__ExcelDir__=__StaticDir__+"/excel/"
__Add_info__=__StaticDir__+"/add_info/"
#initiate the app
appME=Flask(__name__) #__name__=app
appME.config.from_object('config')

#initiate the database
db = SQLAlchemy(appME)

# engine=Engine()

#initiate flask-login
lm = LoginManager()
lm.setup_app(appME)


from app import views,models
