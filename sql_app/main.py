from fastapi import Depends, FastAPI, HTTPException

from typing import List
from sqlalchemy.orm import Session

from .models import *
from . import crud, models, schemas
from .database import local_session
from sql_app import database
from fastapi.responses import StreamingResponse
import pandas
import io

# models.Base.metadata.create_all(bind=old_engine)

# models.Base.metadata.create_all(bind=new_engine)

app = FastAPI()


# Dependency
def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def get_home():
    return 'Hello World'

@app.get("/mt4orders")
def get_4orders(db: Session = Depends(get_db)):
    orders = db.query(MT4OpenOrders).all()
    return orders

@app.get("/mt5orders")
def get_5orders(db: Session = Depends(get_db)):
    orders = db.query(MT5OpenOrders).all()
    return orders

# crm4_Rebate_And_Email_check
# @app.get("/parentCheck")
# def read_crm4_accs(db: Session = Depends(get_db)):
#     temp = []
#     i = 0
#     for crm4_accs in db.query(OldMT4Account.login, Old4User.email, OldMT4Account.login_type, Old4User.parent_id).filter(OldMT4Account.user_id == Old4User.id).all():
        
#         if crm4_accs[2]=='2':
#             acc_type = "Rebate Acc"
#         elif crm4_accs[2]=='1':
#             acc_type = "Trade Acc"
#         else:
#             acc_type = "Something Wrong"
#         crm4_parent_id = crm4_accs[3]
#         crm4_parent = db.query( Old4User.email, OldMT4Account.login,).filter(Old4User.id == crm4_parent_id).join(OldMT4Account).first()
        
        
#         if crm4_parent == None:
#             crm4_parent = ("No Parent MT or SuperAdmin", "No Parent Email")
        
#         new_crm = db.query(NewMTAccount.mt_account, NewTAInfo.email_Plaintext, NewTAInfo.parent_ib, NewTAInfo.parent_type, NewTAInfo.ta_type).filter(NewMTAccount.mt_account == crm4_accs[0]).join(NewTAInfo).first()
        
        
        
#         # if crm4_accs[0] == None:
#         #     crm4_accs[0] = "No Commision"
#         # if crm4_accs[1] == None:
#         #     crm4_accs[1] = "No Email"
#         # if crm4_parent[0] == None:
#         #     crm4_parent[0] = "No Parent Rebate Acc"
#         # if crm4_parent[1] == None:
#         #     crm4_parent[1] = "No Parent Email"
        
        
#         if new_crm == None:
#             if crm4_accs[2]=='2':
#                 new_crm = ("No Rebate Acc", "No Email", "Parent_IB not Exist", "Parnet_Type not Exist", "TA Type")
#             if crm4_accs[2]=='1':
#                 new_crm = ("No Trade Acc", "No Email", "Parent_IB not Exist", "Parnet_Type not Exist", "TA Type")
        
            
#         if new_crm[4] == 1: #1 IS IB's TA Acc
#             new_crm_parent_id = new_crm[2]
#             new_crm_ib = db.query(NewIBInfo.email_Plaintext, NewIBInfo.parent_id).filter(
#                 NewIBInfo.id == new_crm_parent_id
#             ).first()
            
            
#             new_crm_parent_type = new_crm[3] #1 is AM and 2 is IB
            
#             # # print("Check Type", new_crm_parent_type)
#             if new_crm_parent_type == 2 and new_crm_ib != None: #For IB
#                 # print("Ash999-Debuggggggg")
#                 new_real_parent_id = new_crm_ib[1]
#                 # print("1--", new_real_parent_id)
#                 new_crm_parent = db.query(NewIBInfo.email_Plaintext).filter(NewIBInfo.id == new_real_parent_id).first()
#                 # print("2--", new_crm_parent)
#                 if new_crm_parent == None:
#                     new_crm_parent = ("IB Not Exist", "IB Null")
                
#                 # print("IB Parent in New CRM = ", new_crm_parent[0], ' id ')
            
#             if new_crm_parent_type == 1 and new_crm_ib != None:
#                 new_crm_parent = db.query(NewSYSUser.email_Plaintext).filter(NewSYSUser.id == new_crm_ib).first()
                
#                 if new_crm_parent == None:
#                     new_crm_parent = ("AM Not Exist", "AM Null")
#                 # print("AM Parent in New CRM =", new_crm_parent[0], ' id ')
                
#         if new_crm[4] == 2:
#             new_crm_parent_id = new_crm[2]
#             new_crm_parent_type = new_crm[3]
            
#             if new_crm_parent_type == 2: #For IB
#                 new_crm_parent = db.query(NewIBInfo.email_Plaintext).filter(NewIBInfo.id == new_crm_parent_id).first()
                
#                 if new_crm_parent == None:
#                     new_crm_parent = ("IB Not Exist")
                
#                 # print("IB Parent in New CRM = ", new_crm_parent[0], ' id ', new_crm_parent_id)
            
#             if new_crm_parent_type == 1:
#                 new_crm_parent = db.query(NewSYSUser.email_Plaintext).filter(NewSYSUser.id == new_crm_parent_id).first()
                
#                 if new_crm_parent == None:
#                     new_crm_parent = ("AM Not Exist")
#                 # print("AM Parent in New CRM =", new_crm_parent[0], ' id ', new_crm_parent_id)
            
#         # TODO: Need to check with contain
#         if crm4_accs[1] == new_crm[1]:
#             dc_email_same = "DC Email Same"
#         elif crm4_accs[1] != new_crm[1]:
#             dc_email_same = "DC Email Not Same"
        
#         if crm4_parent[0] == new_crm_parent[0]:
#             parent_email_same = "Parent Email Same"
#         elif crm4_parent[0] != new_crm_parent[0]:
#             parent_email_same = "Parent Email Not Same"
        
#         write_data = ( acc_type, crm4_accs[0], new_crm[0], crm4_accs[1], new_crm[1], crm4_parent[0],
#                       new_crm_parent[0], dc_email_same, parent_email_same
#                       )
        
#         i = i + 1
#         # print(i)
#         # print(write_data)
        
#         temp.append(write_data)
#         ## print(temp)
    
#     df = pandas.DataFrame(temp, columns=['mt4_acc_type', 'mt4_acc',  'newcrm_acc', 'mt4_mail', 'newcrm_email',  'mt4_parent_email', 'new_crm_parent_email', 'DC Email Flag', 'Parent Email Flag'
#                                          ])

    
#     # df = pandas.DataFrame(temp, columns=['mt4_acc', 'mt4_mail', 'mt4_parent_acc', 'mt4_parent_email', 'newcrm_acc', 'newcrm_email', 'newcrm_parent_acc', 'newcrm_parent_email', 'dcsame_flag', 'parentsame_flag' ])
    
#     stream = io.StringIO()
#     df.to_csv(stream, index=False)
#     response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
#     response.headers["Content-Disposition"] = "attachment; filename=crm4_Parent_check.csv"
#     return response


# @app.get("/file")
# async def export_excel(db: Session = Depends(get_db)):
#     oldAccs = db.query(OldMT5Account.login).all()
#     newAccs = db.query(NewMTAccount.mt_account).all()
    
   
#     df = pandas.DataFrame( zip(oldAccs,newAccs), columns=['login', 'newAccs'])
    
    
#     stream = io.StringIO()
#     df.to_csv(stream, index= False)
#     response = StreamingResponse(iter([stream.getvalue()]),
#                                  media_type="text/csv"
#                                  )
#     response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    
#     return response