from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.automap import automap_base

# With SQL Lite
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# With postgresql
OLD_CRM_URL = "mysql+mysqlconnector://root:admin123@localhost:3306/crm5_db"
NEW_CRM_URL = "mysql+mysqlconnector://root:admin123@localhost:3306/new_crm_db_27"
# With PostgreSQL
old_engine = create_engine(
    OLD_CRM_URL
)
old_local = sessionmaker(autocommit=False, autoflush=False, bind=old_engine)
new_engine = create_engine(
    NEW_CRM_URL
)
new_local = sessionmaker(autocommit=False,  autoflush=False, bind=new_engine)


BaseOld = declarative_base()
BaseNew = declarative_base()

local_session = sessionmaker()
local_session.configure(binds={
    BaseOld: old_engine,
    BaseNew: new_engine
})
    

