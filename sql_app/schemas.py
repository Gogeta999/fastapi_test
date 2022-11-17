"""
To avoid confusion between the SQLAlchemy models and the Pydantic models, we will have the file models.py with the SQLAlchemy models, and the file schemas.py with the Pydantic models.

These Pydantic models define more or less a "schema" (a valid data shape).

So this will help us avoiding confusion while using both.
"""
from datetime import datetime
from pydantic import BaseModel

class OldMT4Account(BaseModel):
    login: int | None
    user_id: int | None
    login_type: str | None
    # commit_group_id: int | None
    
    class Config:
        orm_mode = True 
 
class Old4User(BaseModel):
    id: int # user id
    user_name: str
    parent_id: int #User Parent ID
    role_id: int #2 is Agent, 3 is DC
    email: str | None

    class Config:
        orm_mode = True 


class OldMT5Account(BaseModel):
    login: int | None
    user_id: int | None
    login_type: str | None
    # commit_group_id: int | None
    # create_time: datetime | None
    # update_time: datetime | None
    
    class Config:
        orm_mode = True 
 
class Old5User(BaseModel):
    id: int # user id
    user_name: str
    parent_id: int #User Parent ID
    role_id: int #2 is Agent, 3 is DC
    email: str | None
    
    # user_code: str | None
    # password: str | None
    # role_group_id: int | None
    # channel_id: int | None
    # parent_id: int | None
    # photo: str | None
    # phone: str | None
    # commit_level_id: str | None
    # commit_rule_param: str | None
    # reg_time: datetime | None
    # u_status: int | None
    # info_status: int | None
    # info_review_status: int | None
    # language: str | None
    # invit_code: str | None
    # totp_secret: str | None
    # login_fail_count: int | None
    # last_login_time: datetime | None
    # deposit_group_id: int | None
    # login_verify_code: str | None
    
    class Config:
        orm_mode = True 

class NewMTAccount(BaseModel):
    id: str
    ta_user_id: str | int | None
    mt_account: int
    account_name: str | None
    account_group: str
    mt_group: str
    mt_acct_type_id: str
    is_main_account: int | None #Is Auto Created by System or Not
    mt_server: int  # 40 is MT4 demo, 41 is MT4 real, 50 is MT5 Demo, 51 is MT5 Real
    
    # leverage: str | None
    # open_date: datetime | None
    # deal_status: int | None
    # enabled_status: int | None
    # enabled_date: datetime | None
    # enable_change_password: int | None
    # enable_otp: int | None
    # settlement_type: str | None
    # rebate_group_id: str | None
    # create_date: datetime | None
    # create_userid: str | None
    # create_name: str | None
    # modify_date: datetime | None
    # modify_userid: str | None
    # modify_name: str | None
    # remarks: str | None
    
    class Config:
        orm_mode = True 
        
class NewTAInfo(BaseModel):
    id: str #aka ta_user_id from MT Acc
    email: str
    name: str
    mt_name: str | None #Name From MT
    parent_ib: str | None #Superior IB or AM
    parent_type: int # 1 isAM and 2 is IB
    ta_type: int # 1 is Agent TA, 2 is Pure TA
    email_Plaintext = str
    
    # ident_code: str | None
    # pwd: str | None
    # tel: str | None
    # tel_prefix: str | None
    # tel_is_verify: int | None
    # sex: int | None
    # birthday: str | None
    # nation_id: int | None
    # nation: str | None
    # province: str | None
    # city: str | None
    # county: str | None
    # address: str | None
    # avatar: str | None
    # zip: str | None
    # status: int | None
    # open_acct_status: int | None
    # open_acct_time: datetime | None
    # lock_time: datetime | None
    # mt_servers: str | None
    # payment_group_id: str | None
    # lang: str | None
    # create_date: datetime | None
    # create_userid: str | None
    # create_name: str | None
    # modify_date: datetime | None
    # modify_userid: str | None
    # modify_name: str | None
    # remarks: str | None
    # deleted: int | None
    # delete_date: datetime | None
    # delete_userid: str | None
    # delete_name: str | None
    # superior_code: str | None
    # is_send: int | None
    
    class Config:
        orm_mode = True 

class NewIBInfo(BaseModel):
    id: str #from ta's parent_ib
    email: str
    email_Plaintext: str
    name: str
    mt_name: str
    ib_type: str # IB or SubIB
    ib_level_id: str # ib in ib level id
    parent_id: str # if this is MIB than this id will be SYS id if not IB id
    ta_id: str #id from his ta table
    mt4_account_id: str #rebate for MT4
    mt5_account_id: str #rebate for MT5
    root_ib_id: str #if this id same as own id, than his is mib. if blank than his is 无归属IB
    
    class Config:
        orm_mode = True 
 
class NewSYSUser(BaseModel):
    id: str #aka parent_ib from TA Info
    login_name:str #most am using Email and login
    real_name: str #different name
    english_name: str #name
    main_depart_id: str | None
    main_depart_name:str  | None
    job_post_ids: str | None
    job_post_names:str | None #his role 
    report_user_id:str | None #superior
    report_user_name:str | None #superior name
    
    # unique_id: str | None
    # login_pwd: str | None
    # avatar: str | None
    # sex: int | None
    # status: int | None
    # subsidiary_depart_ids: str | None
    # subsidiary_depart_names: str | None
    # rebate_level_id: str | None
    # qq: str | None
    # wx: str | None
    # email: str | None
    # office_tel: str | None
    # mobile_phone: str | None
    # login_status: int | None
    # birthday: datetime | None
    # user_number: str | None
    # entry_time: datetime | None
    # lock_time: datetime | None
    # locked_count: int | None
    # create_date: datetime | None
    # create_user: str | None
    # create_userid: str | None
    # modify_date: datetime | None
    # modify_userid: str | None
    # modify_name: str | None
    # remarks: str | None
    # delete_date: datetime | None
    # delete_userid: str | None
    # delete_name: str | None
    # deleted: int | None
    # google_sk: str | None
    # google_auth_band: int | None
    # google_yz_firsttime: datetime | None
    # google_yz_count: int | None
    # google_yz_disable: int | None
    
    class Config:
        orm_mode = True 

class MT4OpenOrders(BaseModel):
    ID : str
    Activation : int | None
    ClosePrice : float | None
    CloseTime : datetime | None
    Cmd : int | None
    Comment : str | None
    Commission : float | None
    CommissionAgent : float | None
    Digits : int | None
    Expiration : datetime | None
    GwClosePrice : int | None
    GwOpenPrice : int | None
    GwOrder : int | None
    GwVolume : int | None
    Login : int | None
    Magic : int | None
    MarginRate : float | None
    OpenPrice : float | None
    OpenTime : datetime | None
    OrderNum : int | None
    Profit : float | None
    Reason : int | None
    Sl : float | None
    State : int | None
    Storage : float | None
    Symbol : str | None
    Taxes : float | None
    Timestamp : str | None
    Tp : float | None
    Volume : int | None
    UserId : str | None
    UserName : str | None
    BelongId : str | None
    BelongName : str | None
    SymbolGroupId : str | None
    SymbolGroupName : str | None
    SalseID : str | None
    SalseName : str | None
    MTServer : int | None
    Mt_group_alias : str | None
    class Config:
        
        orm_mode = True
        
class MT5OpenOrders(BaseModel):
    ID : str
    Activation : int | None
    ClosePrice : float | None
    CloseTime : datetime | None
    Cmd : int | None
    Comment : str | None
    Commission : float | None
    CommissionAgent : float | None
    Digits : int | None
    Expiration : datetime | None
    GwClosePrice : int | None
    GwOpenPrice : int | None
    GwOrder : int | None
    GwVolume : int | None
    Login : int | None
    Magic : int | None
    MarginRate : float | None
    OpenPrice : float | None
    OpenTime : datetime | None
    OrderNum : int | None
    Profit : float | None
    Reason : int | None
    Sl : float | None
    State : int | None
    Storage : float | None
    Symbol : str | None
    Taxes : float | None
    Timestamp : str | None
    Tp : float | None
    Volume : int | None
    UserId : str | None
    UserName : str | None
    BelongId : str | None
    BelongName : str | None
    SymbolGroupId : str | None
    SymbolGroupName : str | None
    SalseID : str | None
    SalseName : str | None
    MTServer : int | None
    Mt_group_alias : str | None
    class Config:
        
        orm_mode = True