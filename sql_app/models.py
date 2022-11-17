from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Float
from sqlalchemy.orm import relationship

from .database import BaseOld5, BaseNew, BaseOld4

class OldMT4Account(BaseOld4):
    __tablename__ = "mt_account"
    login = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    login_type = Column(String(255))
    # commit_group_id = Column(Integer)
    # create_time = Column(DateTime)
    # update_time = Column(DateTime)
    
    
    # owner_id = Column(Integer, ForeignKey("users.id"))
    # owner = relationship("Old5User", back_populates="accs")

class Old4User(BaseOld4):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255))
    parent_id = Column(Integer)
    role_id = Column(Integer)
    email = Column(String(255))

class OldMT5Account(BaseOld5):
    __tablename__ = "mt_account"
    login = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    login_type = Column(String(255))
    # commit_group_id = Column(Integer)
    # create_time = Column(DateTime)
    # update_time = Column(DateTime)
    
    
    # owner_id = Column(Integer, ForeignKey("users.id"))
    # owner = relationship("Old5User", back_populates="accs")

class Old5User(BaseOld5):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(255))
    parent_id = Column(Integer)
    role_id = Column(Integer)
    email = Column(String(255))
   
    
    # accs = relationship("OldMT5Account", back_populates="owner")

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
    email_Plaintext = Column(String(255))
    
class NewIBInfo(BaseNew):
    __tablename__ = "ib_base_info"
    id = Column(String(36), primary_key=True, index=True)
    email = Column(String(255))
    email_Plaintext = Column(String(255))
    name = Column(String(100))
    mt_name = Column(String(50))
    ib_type = Column(String(30))
    ib_level_id = Column(String(36))
    parent_id = Column(String(36))
    ta_id = Column(String(36))
    mt4_account_id = Column(String(36))
    mt5_account_id = Column(String(36))
    root_ib_id = Column(String(36))

class NewSYSUser(BaseNew):
    __tablename__ = "sys_users"
    id = Column(String(36), primary_key=True, index=True) #aka parent_ib from TA Info
    email_Plaintext = Column(String(255))
    login_name = Column(String(255))
    real_name = Column(String(50))
    english_name = Column(String(50))
    main_depart_id = Column(String(36))
    main_depart_name = Column(String(50))
    job_post_names = Column(Text)
    report_user_id = Column(String(36))
    report_user_name = Column(String(50))

class MT4OpenOrders(BaseNew):
    __tablename__ = "tradeorderopen"
    
    ID = Column(String(36), primary_key=True, index=True)
    Activation = Column(Integer)
    ClosePrice = Column(Float)
    CloseTime = Column(DateTime)
    Cmd = Column(Integer)
    Comment = Column(Text)
    Commission = Column(Float)
    CommissionAgent = Column(Float)
    Digits = Column(Integer)
    Expiration = Column(DateTime)
    GwClosePrice = Column(Integer)
    GwOpenPrice = Column(Integer)
    GwOrder = Column(Integer)
    GwVolume = Column(Integer)
    Login = Column(Integer)
    Magic = Column(Integer)
    MarginRate = Column(Float)
    OpenPrice = Column(Float)
    OpenTime = Column(DateTime)
    OrderNum = Column(Integer)
    Profit = Column(Float)
    Reason = Column(Integer)
    Sl = Column(Float)
    State = Column(Integer)
    Storage = Column(Float)
    Symbol = Column(Text)
    Taxes = Column(Float)
    Timestamp = Column(String(50))
    Tp = Column(Float)
    Volume = Column(Integer)
    UserId = Column(String(36))
    UserName = Column(String(100))
    BelongId = Column(String(36))
    BelongName = Column(String(128))
    SymbolGroupId = Column(String(36))
    SymbolGroupName = Column(String(100))
    SalseID = Column(String(36))
    SalseName = Column(String(100))
    MTServer = Column(Integer)
    Mt_group_alias = Column(String(30))


class MT5OpenOrders(BaseNew):
    __tablename__ = "tradeorderopen_mt5"
    
    ID = Column(String(36), primary_key=True, index=True)
    Activation = Column(Integer)
    ClosePrice = Column(Float)
    CloseTime = Column(DateTime)
    Cmd = Column(Integer)
    Comment = Column(Text)
    Commission = Column(Float)
    CommissionAgent = Column(Float)
    Digits = Column(Integer)
    Expiration = Column(DateTime)
    GwClosePrice = Column(Integer)
    GwOpenPrice = Column(Integer)
    GwOrder = Column(Integer)
    GwVolume = Column(Integer)
    Login = Column(Integer)
    Magic = Column(Integer)
    MarginRate = Column(Float)
    OpenPrice = Column(Float)
    OpenTime = Column(DateTime)
    OrderNum = Column(Integer)
    Profit = Column(Float)
    Reason = Column(Integer)
    Sl = Column(Float)
    State = Column(Integer)
    Storage = Column(Float)
    Symbol = Column(Text)
    Taxes = Column(Float)
    Timestamp = Column(String(50))
    Tp = Column(Float)
    Volume = Column(Integer)
    UserId = Column(String(36))
    UserName = Column(String(100))
    BelongId = Column(String(36))
    BelongName = Column(String(128))
    SymbolGroupId = Column(String(36))
    SymbolGroupName = Column(String(100))
    SalseID = Column(String(36))
    SalseName = Column(String(100))
    MTServer = Column(Integer)
    Mt_group_alias = Column(String(30))