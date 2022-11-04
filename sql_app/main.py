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

@app.get("/oldAccs")
def read_old_accs(db: Session = Depends(get_db)):
    
    accs = db.query(OldMTAccount.user_id, OldUser.email, OldMTAccount.login, OldMTAccount.login_type, OldUser.parent_id).join(OldUser).all()
    
    for acc in db.query(OldMTAccount.user_id, OldUser.email, OldMTAccount.login, OldMTAccount.login_type, OldUser.parent_id).join(OldUser):
        # acc = 1  + acc
        print(type(acc))
   
    return accs

# @app.get("/oldUsers", response_model=List[schemas.OldUser])
# def read_old_accs(db: Session = Depends(get_db)):
#     return db.query(OldUser).all()

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
    oldAccs = db.query(OldMTAccount.login).all()
    newAccs = db.query(NewMTAccount.mt_account).all()
    
   
    df = pandas.DataFrame( zip(oldAccs,newAccs), columns=['login', 'newAccs'])
    
    
    stream = io.StringIO()
    df.to_csv(stream, index= False)
    response = StreamingResponse(iter([stream.getvalue()]),
                                 media_type="text/csv"
                                 )
    response.headers["Content-Disposition"] = "attachment; filename=export.csv"
    
    return response