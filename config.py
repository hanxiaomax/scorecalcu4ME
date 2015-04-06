import os
basedir=os.path.abspath(os.path.dirname(__file__))#get basedir of the project

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-guess'

#for database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#for upload pic
UPLOAD_FOLDER = basedir+'/uploads/' #should use basedir
MAX_CONTENT_LENGTH=2*1024*1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])#TODO:make user aware

#for upload excel
UPLOAD_EXCEL = basedir+'/app/static/add_info/' #should use basedir
