from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
score_items = Table('score_items', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('catagory', VARCHAR(length=140)),
    Column('item_name', VARCHAR(length=120)),
    Column('time', VARCHAR(length=140)),
    Column('user_id', INTEGER),
    Column('add', FLOAT),
    Column('applytime', VARCHAR(length=30), nullable=False),
    Column('status', SMALLINT),
    Column('picpath', VARCHAR(length=140)),
    Column('uuid', VARCHAR(length=64)),
)

score_items = Table('score_items', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('catagory', String(length=140)),
    Column('item_name', String(length=120)),
    Column('time_st', String(length=30)),
    Column('time_ed', String(length=30)),
    Column('add', Float),
    Column('applytime', String(length=30)),
    Column('status', SmallInteger, default=ColumnDefault(2)),
    Column('picpath', String(length=140)),
    Column('user_id', Integer),
    Column('uuid', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['score_items'].columns['time'].drop()
    post_meta.tables['score_items'].columns['time_ed'].create()
    post_meta.tables['score_items'].columns['time_st'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['score_items'].columns['time'].create()
    post_meta.tables['score_items'].columns['time_ed'].drop()
    post_meta.tables['score_items'].columns['time_st'].drop()
