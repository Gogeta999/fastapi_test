"""
To avoid confusion between the SQLAlchemy models and the Pydantic models, we will have the file models.py with the SQLAlchemy models, and the file schemas.py with the Pydantic models.

These Pydantic models define more or less a "schema" (a valid data shape).

So this will help us avoiding confusion while using both.
"""
from datetime import datetime
from pydantic import BaseModel

class OldMTAccount(BaseModel):
    login: int | None = None
    user_id: int | None = None
    login_type: str | None = None
    commit_group_id: int | None = None
    create_time: datetime | None = None
    update_time: datetime | None = None
    
    class Config:
        orm_mode = True 
 
class OldUser(BaseModel):
    id: int # user id
    user_name: str
    parent_id: int #User Parent ID
    role_id: int #2 is Agent, 3 is DC

    user_code: str | None
    password: str | None
    email: str | None
    role_group_id: int | None
    channel_id: int | None
    parent_id: int | None
    photo: str | None
    phone: str | None
    commit_level_id: str | None
    commit_rule_param: str | None
    reg_time: datetime | None
    u_status: int | None
    info_status: int | None
    info_review_status: int | None
    language: str | None
    invit_code: str | None
    totp_secret: str | None
    login_fail_count: int | None
    last_login_time: datetime | None
    deposit_group_id: int | None
    login_verify_code: str | None
    
    class Config:
        orm_mode = True 

class NewMTAccount(BaseModel):
    id: str
    ta_user_id: str | int | None
    mt_account: int
    account_name: str | None = None
    account_group: str
    mt_group: str
    mt_acct_type_id: str
    is_main_account: int | None = None #Is Auto Created by System or Not
    mt_server: int  # 40 is MT4 demo, 41 is MT4 real, 50 is MT5 Demo, 51 is MT5 Real
    
    leverage: str | None = None
    open_date: datetime | None = None
    deal_status: int | None = None
    enabled_status: int | None = None
    enabled_date: datetime | None = None
    enable_change_password: int | None = None
    enable_otp: int | None = None
    settlement_type: str | None = None
    rebate_group_id: str | None = None
    create_date: datetime | None = None
    create_userid: str | None = None
    create_name: str | None = None
    modify_date: datetime | None = None
    modify_userid: str | None = None
    modify_name: str | None = None
    remarks: str | None = None
    
    class Config:
        orm_mode = True 
        
class NewTAInfo(BaseModel):
    id: str #aka ta_user_id from MT Acc
    email: str
    name: str
    mt_name: str #Name From MT
    parent_ib: str #Superior IB or AM
    parent_type: int # 1 isAM and 2 is IB
    ta_type: int # 1 is Agent TA, 2 is Pure TA
    
    
    ident_code: str | None
    pwd: str | None
    tel: str | None
    tel_prefix: str | None
    tel_is_verify: int | None
    sex: int | None
    birthday: str | None
    nation_id: int | None
    nation: str | None
    province: str | None
    city: str | None
    county: str | None
    address: str | None
    avatar: str | None
    zip: str | None
    status: int | None
    open_acct_status: int | None
    open_acct_time: datetime | None
    lock_time: datetime | None
    mt_servers: str | None
    payment_group_id: str | None
    lang: str | None
    create_date: datetime | None
    create_userid: str | None
    create_name: str | None
    modify_date: datetime | None
    modify_userid: str | None
    modify_name: str | None
    remarks: str | None
    deleted: int | None
    delete_date: datetime | None
    delete_userid: str | None
    delete_name: str | None
    superior_code: str | None
    is_send: int | None
    
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
    
    unique_id: str | None
    login_pwd: str | None
    avatar: str | None
    sex: int | None
    status: int | None
    subsidiary_depart_ids: str | None
    subsidiary_depart_names: str | None
    rebate_level_id: str | None
    qq: str | None
    wx: str | None
    email: str | None
    office_tel: str | None
    mobile_phone: str | None
    login_status: int | None
    birthday: datetime | None
    user_number: str | None
    entry_time: datetime | None
    lock_time: datetime | None
    locked_count: int | None
    create_date: datetime | None
    create_user: str | None
    create_userid: str | None
    modify_date: datetime | None
    modify_userid: str | None
    modify_name: str | None
    remarks: str | None
    delete_date: datetime | None
    delete_userid: str | None
    delete_name: str | None
    deleted: int | None
    google_sk: str | None
    google_auth_band: int | None
    google_yz_firsttime: datetime | None
    google_yz_count: int | None
    google_yz_disable: int | None
# class ItemBase(BaseModel):
#     title: str
#     description: str | None = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: list[Item] = []

#     class Config:
#         orm_mode = True
