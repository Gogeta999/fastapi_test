from fastapi import Depends, APIRouter
from datetime import datetime, timedelta
from sql_app.database import local_session, pure_session
import json
from datetime import datetime, timedelta
from decimal import *
from sqlalchemy.orm import Session
from sqlalchemy import text
from sql_app.models import *

def get_db():
    db = local_session()
    try:
        yield db
    finally:
        db.close()
      
def pure_sql():
    db = pure_session()
    try:
        yield db
    finally:
        db.close()

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        # if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        #otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)
  
router = APIRouter()

@router.get("/mt4positions")
async def mt4_positions(db: Session = Depends(get_db)):
    orders = db.query(MT4OpenOrders).all()
    return orders

@router.get("/mt5positions")
async def mt5_positions(db: Session = Depends(get_db)):
    orders = db.query(MT5OpenOrders).all()
    return orders

@router.get("/mtacc")
async def mt_accs(db: Session = Depends(pure_sql)):
    sql = text("SELECT * FROM mt_accounts")
    sql_results = db.execute(sql)
    print("SQL Res", sql_results)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@router.get("/mt4orders")
async def mt4_orders(db: Session= Depends(pure_sql), before_day: int = 7):
    time_delta = timedelta(days=before_day)
    expect_time = (datetime.now() - time_delta).strftime("%Y-%m-%d %H:%M:%S")
    sql = text("SELECT  trade.Login, trade.Cmd, trade.Symbol, trade.Volume, trade.OpenPrice, trade.ClosePrice, trade.OpenTime, trade.CloseTime, trade.Commission, trade.`Storage`, trade.Profit, trade.OrderNum, trade.BelongName, trade.MTServer   FROM traderecord as trade WHERE CloseTime > :date")
    sql_results = db.execute(sql, {'date': expect_time})
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@router.get("/mt5orders")
async def mt5_orders(db: Session= Depends(pure_sql), before_day: int = 7):
    time_delta = timedelta(days=before_day)
    expect_time = (datetime.now() - time_delta).strftime("%Y-%m-%d %H:%M:%S")
    sql = text("SELECT  trade.Login, trade.Cmd, trade.Symbol, trade.Volume, trade.OpenPrice, trade.ClosePrice, trade.OpenTime, trade.CloseTime, trade.Commission, trade.`Storage`, trade.Profit, trade.OrderNum, trade.BelongName, trade.MTServer  FROM traderecord_mt5 WHERE CloseTime > :date")
    sql_results = db.execute(sql, {'date': expect_time})
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@router.get("/deposit")
async def deposit_record(db: Session = Depends(pure_sql)):
    sql = text("SELECT ta.mt_account, ta.deposit_dollar, ta.fund_type, ta.belong_ib_name, ta.belong_sale_name, ta.fund_remark, ta.mt_server, ta.create_date  FROM ta_finance_records as ta WHERE ta.deposit_dollar > 0")
    sql_results = db.execute(sql)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@router.get("/withdraw")
async def withdraw_record(db: Session = Depends(pure_sql)):
    sql = text("SELECT ta.mt_account, ta.withdraw_dollar, ta.fund_type, ta.belong_ib_name, ta.belong_sale_name, ta.fund_remark, ta.mt_server, ta.create_date  FROM ta_finance_records as ta WHERE ta.withdraw_dollar > 0")
    sql_results = db.execute(sql)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@router.get("/adjust")
async def adjust_record(db: Session = Depends(pure_sql)):
    sql = text("SELECT ta.mt_account, ta.adjust_dollar, ta.fund_type, ta.belong_ib_name, ta.belong_sale_name, ta.fund_remark, ta.mt_server, ta.create_date  FROM ta_finance_records as ta WHERE ta.adjust_dollar > 0")
    sql_results = db.execute(sql)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@router.get("/transfer_records")
async def trasfer_record(db: Session= Depends(pure_sql), before_day: int = 7):
    time_delta = timedelta(days=before_day)
    expect_time = (datetime.now() - time_delta).strftime("%Y-%m-%d %H:%M:%S")
    sql = text("SELECT * FROM ta_transfer_records")
    sql_results = db.execute(sql)
    #sql_results = db.execute(sql, {'date': expect_time})
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@router.get("/rebate_tradecomm")
async def rebate_record(db: Session= Depends(pure_sql), before_day: int = 7):
    time_delta = timedelta(days=before_day)
    expect_time = (datetime.now() - time_delta).strftime("%Y-%m-%d %H:%M:%S")
    sql = text("SELECT * FROM rebate_tradecomm WHERE CloseTime > :date")
    sql_results = db.execute(sql, {'date': expect_time})
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results
    
@router.get("/profit")
async def profit_record(db: Session= Depends(pure_sql), before_day: int = 7):
    time_delta = timedelta(days=before_day)
    expect_time = (datetime.now() - time_delta).strftime("%Y-%m-%d %H:%M:%S")
    sql = text("SELECT * FROM rebate_tradecomm WHERE CloseTime > :date")
    sql_results = db.execute(sql, {'date': expect_time})
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results