from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
post = Table('post', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('body', VARCHAR(length=140)),
    Column('timestamp', DATETIME),
    Column('user_id', INTEGER),
)

score = Table('score', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('body', String(length=140)),
    Column('timestamp', DateTime),
    Column('user_id', Integer),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('nickname', VARCHAR(length=64)),
    Column('email', VARCHAR(length=120)),
    Column('role', SMALLINT),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('campID', String(length=120)),
    Column('password', String(length=120)),
    Column('Class', Integer),
    Column('grade', String(length=64)),
    Column('role', SmallInteger, default=ColumnDefault(0)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].drop()
    post_meta.tables['score'].create()
    pre_meta.tables['user'].columns['email'].drop()
    pre_meta.tables['user'].columns['nickname'].drop()
    post_meta.tables['user'].columns['Class'].create()
    post_meta.tables['user'].columns['campID'].create()
    post_meta.tables['user'].columns['grade'].create()
    post_meta.tables['user'].columns['name'].create()
    post_meta.tables['user'].columns['password'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['post'].create()
    post_meta.tables['score'].drop()
    pre_meta.tables['user'].columns['email'].create()
    pre_meta.tables['user'].columns['nickname'].create()
    post_meta.tables['user'].columns['Class'].drop()
    post_meta.tables['user'].columns['campID'].drop()
    post_meta.tables['user'].columns['grade'].drop()
    post_meta.tables['user'].columns['name'].drop()
    post_meta.tables['user'].columns['password'].drop()
