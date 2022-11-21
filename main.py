from fastapi import Depends, FastAPI, HTTPException

from typing import List
from sqlalchemy.orm import Session

from sql_app.models import *
from sql_app import crud, models, schemas
from sql_app.database import local_session
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
async def get_4orders(db: Session = Depends(get_db)):
    orders = db.query(MT4OpenOrders).all()
    return orders

@app.get("/mt5orders")
async def get_5orders(db: Session = Depends(get_db)):
    orders = db.query(MT5OpenOrders).all()
    return orders