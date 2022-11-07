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

# crm4_check
@app.get("/crm4")
def read_crm4_accs(db: Session = Depends(get_db)):
    temp = []
    for crm4_accs in db.query(OldMT4Account.login, Old4User.email, OldMT4Account.login_type, Old4User.parent_id).join(Old4User).limit(5):
        crm4_parent_id = crm4_accs[3]
        crm4_parent = db.query(OldMT4Account.login, Old4User.email).filter(Old4User.id == crm4_parent_id).first()
        
        if crm4_parent == None:
            crm4_parent = ("No Parent MT", "No Parent Email")
        
        new_crm = db.query(NewMTAccount.mt_account, NewTAInfo.email_Plaintext, NewTAInfo.parent_ib, NewTAInfo.parent_type).filter(NewMTAccount.mt_account == crm4_accs[0]).join(NewTAInfo).first()
        
        write_data = (crm4_accs[0], crm4_accs[1], crm4_parent[0], crm4_parent[1],new_crm[0],new_crm[1])
        
        temp.append(write_data)
        print(temp)
    return temp

# crm5_check
@app.get("/test")
def read_old_accs(db: Session = Depends(get_db)):
    temp = []
    
    for acc in db.query(OldMT5Account.login, Old5User.email, OldMT5Account.login_type, Old5User.parent_id).join(Old5User).all():
        # acc = 1  + acc
        
        parent_id = acc[3]
        parent = db.query(OldMT5Account.login, Old5User.email).filter(Old5User.id == parent_id).join(Old5User).first()
        if parent == None:
            parent = ("No Login", "No Email")
        
        
        new_crm = db.query(NewMTAccount.mt_account, NewTAInfo.email_Plaintext, NewTAInfo.parent_ib).filter(NewMTAccount.mt_account==acc[0]).join(NewTAInfo).first()
        
        if new_crm == None:
            new_crm = ("MT Acc Not Exist", "no email", "null")
        
        if new_crm != None:
            new_crm_parent = db.query(NewIBInfo.mt5_account_id, NewIBInfo.email).filter(NewIBInfo.id == new_crm[2]).first()
        
        if new_crm_parent == None:
            new_crm_parent = ("no login", "no email")
        
        dc_same = "DC Mail Not Same"
        if acc[0] == new_crm[0]:
            dc_same = "DC Mail Same"
        parent_same = "Parent Email Not Same"
        if parent[1] == new_crm_parent[1]:
            parent_same = "Parent Email Parent Same"
            
        fill_data = (acc[0], acc[1], parent[0], parent[1],new_crm[0], new_crm[1], new_crm_parent[0], new_crm_parent[1], dc_same, parent_same)
        
        # new_crm_email = base64.b64decode(new_crm_email)
        temp.append(fill_data)
    df = pandas.DataFrame(temp, columns=['old_acc', 'old_email', 'old_parent_acc', 'old_parent_email','new_acc', 'new_email', 'new_parent_acc', 'new_parent_email', 
                                         'dc_same_flag', 'parent_same_flag'])   
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"

    return response

# @app.get("/decrypt")
# def decrypt(db: Session = Depends(get_db)):
#     mt_acc = 88891450
    
#     new_crm = db.query(NewMTAccount.mt_account, NewTAInfo.email_Plaintext).filter(NewMTAccount.mt_account==mt_acc).join(NewTAInfo).first()
#         # print("User ACC", acc[2], "User Email", acc[1], "User Parent Rebate",
#         #       parent[0], "Parent Email", parent[1])
#         # new_crm_email = new_crm[1]
        
#     if new_crm == None:
#             new_crm = ("no login", "no email")
        
#     key = "8de6febcac222e6a915861d644e5cc31"
#     new_crm_email = new_crm[1]
    
#     new_crm_email = new_crm_email.replace('-','+')
#     new_crm_email = new_crm_email.replace('_', '/')

#     mod4 = len(new_crm_email) % 4
        
#     if mod4:
#         add_substr = "===="
#         new_crm_email   = new_crm_email + add_substr[mod4:]
#     new_crm_email = base64.standard_b64decode(new_crm_email).decode("UTF-8", errors="replace")

#     expire = int(new_crm_email[0:10])
#     print(expire)
#     new_crm_email = new_crm_email[10:]
#     print(new_crm_email)
#     sec = int(time.time())
#     print(sec)
#     if (expire > 0 and expire < sec):
#         return ''
#     x = 0
#     len_1 = len(new_crm_email)
#     print(len_1)
#     len_2 = len(key)
#     char = str = ''
    
#     for i in range(len_1):
#         if x == len_2:
#             x = 0
#         char = char + key[x:x+1]
#         x += 1
     
    
#     for i in range(len_1):
#         print(ord(new_crm_email[i:i+1]))
#     #new_crm_email = base64.b64decode(new_crm_email)
    
#     # print(new_crm_email)
#     return 'new_crm_email'

@app.get("/newAccs")
def read_new_accs(db: Session = Depends(get_db)):
    return db.query(NewMTAccount).all() 

@app.get("/newTA")
def read_new_accs(db: Session = Depends(get_db)):
    return db.query(NewTAInfo).all() 

@app.get("/newSYS", response_model=List[schemas.NewSYSUser])
def read_new_accs(db: Session = Depends(get_db)):
    return db.query(NewSYSUser).all() 

@app.get("/file")
async def export_excel(db: Session = Depends(get_db)):
    oldAccs = db.query(OldMT5Account.login).all()
    newAccs = db.query(NewMTAccount.mt_account).all()
    
   
    df = pandas.DataFrame( zip(oldAccs,newAccs), columns=['login', 'newAccs'])
    
    
    stream = io.StringIO()
    df.to_csv(stream, index= False)
    response = StreamingResponse(iter([stream.getvalue()]),
                                 media_type="text/csv"
                                 )
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    
    return response