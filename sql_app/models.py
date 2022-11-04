from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from .database import BaseOld, BaseNew

class OldMTAccount(BaseOld):
    __tablename__ = "mt_account"
    login = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    login_type = Column(String(255))
    # commit_group_id = Column(Integer)
    # create_time = Column(DateTime)
    # update_time = Column(DateTime)
    
    
    # owner_id = Column(Integer, ForeignKey("users.id"))
    # owner = relationship("OldUser", back_populates="accs")

class OldUser(BaseOld):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255))
    parent_id = Column(Integer)
    role_id = Column(Integer)
    email = Column(String(255))
   
    
    # accs = relationship("OldMTAccount", back_populates="owner")

class NewMTAccount(BaseNew):
    __tablename__ = "mt_accounts"
    id = Column(String, primary_key=True, index=True)
    ta_user_id = Column(String(36), ForeignKey("ta_base_info.id"))
    mt_account = Column(Integer)
    account_name = Column(String(50))
    account_group = Column(String(30))
    mt_group = Column(String(50))
    mt_acct_type_id = Column(String(36))
    is_main_account = Column(Integer)  #Is Auto Created by System or Not
    mt_server = Column(Integer) # 40 is MT4 demo, 41 is MT4 real, 50 is MT5 Demo, 51 is MT5 Real
    
class NewTAInfo(BaseNew):
    __tablename__ = "ta_base_info"    
    id = Column(String(36), primary_key=True, index=True) #id from NewMTAcc
    email = Column(String(255))
    name = Column(String(100))
    mt_name = Column(String(255))
    parent_ib = Column(String(36), ForeignKey("sys_users.ib"))  #Superior IB or AM
    parent_type = Column(Integer)  # 1 isAM and 2 is IB 
    ta_type = Column(Integer)  # 1 is Agent TA, 2 is Pure TA
    
class NewSYSUser(BaseNew):
    __tablename__ = "sys_users"
    id = Column(String(36), primary_key=True, index=True) #aka parent_ib from TA Info
    login_name = Column(String(255))
    real_name = Column(String(50))
    english_name = Column(String(50))
    main_depart_id = Column(String(36))
    main_depart_name = Column(String(50))
    job_post_names = Column(Text)
    report_user_id = Column(String(36))
    report_user_name = Column(String(50))
    