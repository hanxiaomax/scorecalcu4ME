from app import db
from app.models import User, Score_items,ROLE_USER, ROLE_ADMIN,STATUS_YES , STATUS_NO , STATUS_UNKNOWN
from datetime import datetime

if __name__ == '__main__':
    user=User.get_user("130280")
    for i in range(1,1000):

        s=Score_items(catagory="_catagory",
        item_name="_name",
        time_st="_time_st",
        time_ed="_time_ed",
        add=3.0,
        applytime="_applytime",
        student=user,
        uuid="_uuid",
        status=STATUS_UNKNOWN
        )


        db.session.add(s)
        print s
    db.session.commit()



