from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
#initiate the app
appME=Flask(__name__) #__name__=app
appME.config.from_object('config')

#initiate the database
db = SQLAlchemy(appME)

#initiate flask-login
lm = LoginManager()
lm.setup_app(appME)


from app import views,models
