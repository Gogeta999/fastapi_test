from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.automap import automap_base

# With SQL Lite
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# With postgresql
# OLD_CRM4_URL = "mysql+mysqlconnector://root:admin123@localhost:3306/crm4_db"
# OLD_CRM5_URL = "mysql+mysqlconnector://root:admin123@localhost:3306/crm5_db"
# NEW_CRM_URL = "mysql+mysqlconnector://root:admin123@localhost:3306/new_crm"
NEW_CRM_URL = "mysql+mysqlconnector://am_rebate_2022:$RK%gB^MPzNNN^8S@rm-gs532b0d90j4zayl9.mysql.singapore.rds.aliyuncs.com:3306/sw_crm"
# With PostgreSQL

# crm4_engine = create_engine(
#     OLD_CRM4_URL
# )
# crm5_engine = create_engine(
#     OLD_CRM5_URL
# )
# old_local = sessionmaker(autocommit=False, autoflush=False, bind=old_engine)
new_engine = create_engine(
    NEW_CRM_URL
)
# new_local = sessionmaker(autocommit=False,  autoflush=False, bind=new_engine)

# BaseOld4 = declarative_base()
# BaseOld5 = declarative_base()
BaseNew = declarative_base()

local_session = sessionmaker()
pure_session = sessionmaker()
local_session.configure(binds={
    # BaseOld4: crm4_engine,
    # BaseOld5: crm5_engine,
    BaseNew: new_engine
})
    
pure_session.configure(bind=new_engine)
