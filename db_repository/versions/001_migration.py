from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
score = Table('score', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('catagory', VARCHAR(length=140)),
    Column('item_name', VARCHAR(length=120)),
    Column('time', DATETIME),
    Column('user_id', INTEGER),
    Column('add', INTEGER),
    Column('standard', INTEGER),
    Column('status', SMALLINT),
)

score_items = Table('score_items', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('catagory', String(length=140)),
    Column('item_name', String(length=120)),
    Column('time', DateTime),
    Column('user_id', Integer),
    Column('add', Integer),
    Column('standard', Integer),
    Column('status', SmallInteger, default=ColumnDefault(2)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['score'].drop()
    post_meta.tables['score_items'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['score'].create()
    post_meta.tables['score_items'].drop()
