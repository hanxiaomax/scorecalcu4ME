from app import db

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index = True)
    campID = db.Column(db.String(120), index = True, unique = True)
    password= db.Column(db.String(120), index = True)
    Class = db.Column(db.Integer,index = True)
    grade= db.Column(db.String(64),index = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    score = db.relationship('Score', backref = 'student', lazy = 'dynamic')
    def __repr__(self):
        return '<User %r>' % (self.name)



    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @classmethod
    def login_check(cls,user_name,password):
        # print user_name
        user = cls.query.filter(db.or_(User.name==user_name, User.password==password)).first()
        # print user
        if not user:
            return None
        return user


class Score(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    reward = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.campID'))

    def __repr__(self):
        return '<Score %r>' % (self.body)
