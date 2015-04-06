from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
excelmap = Table('excelmap', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('Excelname', VARCHAR(length=140)),
    Column('creater', VARCHAR(length=20)),
    Column('start_time', VARCHAR(length=20)),
    Column('end_time', VARCHAR(length=20)),
    Column('creater_time', DATETIME),
    Column('filepath', VARCHAR(length=140)),
    Column('creater_id', INTEGER),
    Column('status', SMALLINT),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['excelmap'].columns['status'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['excelmap'].columns['status'].create()
