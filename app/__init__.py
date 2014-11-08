from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
#initiate the app
app=Flask(__name__) #__name__=app
app.config.from_object('config')

#initiate the database
db = SQLAlchemy(app)

#initiate flask-login
lm = LoginManager()
lm.setup_app(app)


from app import views,models
