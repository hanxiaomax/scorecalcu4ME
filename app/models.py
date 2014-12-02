from app import db

ROLE_USER = 0
ROLE_ADMIN = 1
STATUS_YES = 1
STATUS_NO = 0
STATUS_UNKNOWN= 2
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True)
    campID = db.Column(db.String(120), index = True, unique = True)
    password= db.Column(db.String(120), index = True)
    grade= db.Column(db.String(64),index = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    score_items = db.relationship('Score_items', backref = 'student', lazy = 'dynamic')
    score=db.Column(db.String(10),default="0")

    def __repr__(self):
        return '<User %r>' % (self.name)

    def is_authenticated(self):
        return True

    def is_active(self):
        #Returns True if this is an active user
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @classmethod
    def login_check(cls,user_name,password):
        # print user_name
        user = cls.query.filter(db.and_(User.campID==user_name, User.password==password)).first()
        # print user
        if not user:
            return None
        return user

    @classmethod
    def get_user(cls,campID):
        "get user by campID"
        user = cls.query.filter(db.or_(User.campID==campID)).first()
        if not user:
            return None
        return user





class Score_items(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    catagory = db.Column(db.String(140))
    item_name= db.Column(db.String(120))
    time = db.Column(db.String(140))
    add=db.Column(db.Integer)
    applytime=db.Column(db.String(30))#need to save a formated string
    status= db.Column(db.SmallInteger, default = STATUS_UNKNOWN)
    picpath=db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Score %r>' % (self.time)
