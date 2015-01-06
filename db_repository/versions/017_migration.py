from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
excelmap = Table('excelmap', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('Excelname', String(length=140)),
    Column('creater', String(length=20)),
    Column('creater_id', Integer),
    Column('start_time', String(length=20)),
    Column('end_time', String(length=20)),
    Column('creater_time', DateTime),
    Column('filepath', String(length=140)),
    Column('status', SmallInteger),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['excelmap'].columns['status'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['excelmap'].columns['status'].drop()
