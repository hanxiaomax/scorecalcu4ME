from models import User,Score_items,STATUS_YES
from app import db




if __name__ == '__main__':
    name=u'艾凌风'
    campID="130280"
    user=User.query.filter(User.name==name).first()
    print user
