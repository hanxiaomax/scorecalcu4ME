from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
excelmap = Table('excelmap', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('Excelname', String(length=140)),
    Column('creater', Integer),
    Column('start_time', DateTime),
    Column('end_time', DateTime),
    Column('creater_time', DateTime),
    Column('filepath', String(length=140)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['excelmap'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['excelmap'].drop()
