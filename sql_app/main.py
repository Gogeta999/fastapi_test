from fastapi import Depends, FastAPI, HTTPException

from typing import List
from sqlalchemy.orm import Session
from .models import *
from . import crud, models, schemas
from .database import local_session
from sql_app import database

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

@app.get("/oldAccs", response_model=List[schemas.OldMTAccount])
def read_old_accs(db: Session = Depends(get_db)):
    return db.query(OldMTAccount).all()

@app.get("/oldUsers", response_model=List[schemas.OldUser])
def read_old_accs(db: Session = Depends(get_db)):
    return db.query(OldUser).all()

@app.get("/newAccs", response_model=List[schemas.NewMTAccount])
def read_new_accs(db: Session = Depends(get_db)):
    return db.query(NewMTAccount).all() 

@app.get("/newTAUsers", response_model=List[schemas.NewTAInfo])
def read_new_accs(db: Session = Depends(get_db)):
    return db.query(NewTAInfo).all() 

@app.get("/newAMUsers", response_model=List[schemas.NewSYSUser])
def read_new_accs(db: Session = Depends(get_db)):
    return db.query(NewSYSUser).all() 

# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
