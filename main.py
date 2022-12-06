from fastapi import Depends, FastAPI, HTTPException

from typing import List
from sqlalchemy.orm import Session

from sql_app.models import *
from sql_app import crud, models, schemas
from sql_app.database import local_session, pure_session
from sqlalchemy import text, inspect
from sql_app import database
from fastapi.responses import StreamingResponse
from fastapi.responses import RedirectResponse
import pandas
import io
import json
from datetime import datetime, timedelta
from decimal import *
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


@app.get("/")
def get_home():
    redirect_url = request.url_for('https://pythonapi.mohiash.com/docs') 
    return RedirectResponse(redirect_url, status_code=status.HTTP_303_SEE_OTHER)

@app.get("/mt4positions")
async def mt4_positions(db: Session = Depends(get_db)):
    orders = db.query(MT4OpenOrders).all()
    return orders

@app.get("/mt5positions")
async def mt5_positions(db: Session = Depends(get_db)):
    orders = db.query(MT5OpenOrders).all()
    return orders

@app.get("/mtacc")
async def mt_accs(db: Session = Depends(pure_sql)):
    sql = text("SELECT * FROM mt_accounts")
    sql_results = db.execute(sql)
    print("SQL Res", sql_results)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results



@app.get("/mt4orders")
async def mt4_orders(db: Session= Depends(pure_sql), before_day: int = 7):
    time_delta = timedelta(days=before_day)
    expect_time = (datetime.now() - time_delta).strftime("%Y-%m-%d %H:%M:%S")
    sql = text("SELECT  trade.Login, trade.Cmd, trade.Symbol, trade.Volume, trade.OpenPrice, trade.ClosePrice, trade.OpenTime, trade.CloseTime, trade.Commission, trade.`Storage`, trade.Profit, trade.OrderNum, trade.BelongName, trade.MTServer   FROM traderecord as trade WHERE CloseTime > :date")
    sql_results = db.execute(sql, {'date': expect_time})
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@app.get("/mt5orders")
async def mt5_orders(db: Session= Depends(pure_sql), before_day: int = 7):
    time_delta = timedelta(days=before_day)
    expect_time = (datetime.now() - time_delta).strftime("%Y-%m-%d %H:%M:%S")
    sql = text("SELECT  trade.Login, trade.Cmd, trade.Symbol, trade.Volume, trade.OpenPrice, trade.ClosePrice, trade.OpenTime, trade.CloseTime, trade.Commission, trade.`Storage`, trade.Profit, trade.OrderNum, trade.BelongName, trade.MTServer  FROM traderecord_mt5 WHERE CloseTime > :date")
    sql_results = db.execute(sql, {'date': expect_time})
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

# @app.get("/finance_records")
# async def finance_record(db: Session= Depends(pure_sql), before_day: int = 30):
#     time_delta = timedelta(days=before_day)
#     expect_time = (datetime.now() - time_delta).strftime("%Y-%m-%d %H:%M:%S")
#     sql = text("SELECT ta.mt_account, ta.deposit_dollar, ta.withdraw_dollar, ta.adjust_dollar, ta.fund_type, ta.belong_ib_name, ta.belong_sale_name, ta.fund_remark, ta.mt_server, ta.create_date  FROM ta_finance_records as ta")
#     # sql = text("SELECT * FROM ta_finance_records WHERE create_date > :date")
#     sql_results = db.execute(sql, {'date': expect_time})
#     results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
#     return results

@app.get("/deposit")
async def deposit_record(db: Session = Depends(pure_sql)):
    sql = text("SELECT ta.mt_account, ta.deposit_dollar, ta.fund_type, ta.belong_ib_name, ta.belong_sale_name, ta.fund_remark, ta.mt_server, ta.create_date  FROM ta_finance_records as ta WHERE ta.deposit_dollar > 0")
    sql_results = db.execute(sql)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@app.get("/withdraw")
async def withdraw_record(db: Session = Depends(pure_sql)):
    sql = text("SELECT ta.mt_account, ta.withdraw_dollar, ta.fund_type, ta.belong_ib_name, ta.belong_sale_name, ta.fund_remark, ta.mt_server, ta.create_date  FROM ta_finance_records as ta WHERE ta.withdraw_dollar > 0")
    sql_results = db.execute(sql)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@app.get("/adjust")
async def adjust_record(db: Session = Depends(pure_sql)):
    sql = text("SELECT ta.mt_account, ta.adjust_dollar, ta.fund_type, ta.belong_ib_name, ta.belong_sale_name, ta.fund_remark, ta.mt_server, ta.create_date  FROM ta_finance_records as ta WHERE ta.adjust_dollar > 0")
    sql_results = db.execute(sql)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@app.get("/transfer_records")
async def trasfer_record(db: Session= Depends(pure_sql), before_day: int = 7):
    time_delta = timedelta(days=before_day)
    expect_time = (datetime.now() - time_delta).strftime("%Y-%m-%d %H:%M:%S")
    sql = text("SELECT * FROM ta_transfer_records")
    sql_results = db.execute(sql)
    #sql_results = db.execute(sql, {'date': expect_time})
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@app.get("/rebate_tradecomm")
async def rebate_record(db: Session= Depends(pure_sql), before_day: int = 7):
    time_delta = timedelta(days=before_day)
    expect_time = (datetime.now() - time_delta).strftime("%Y-%m-%d %H:%M:%S")
    sql = text("SELECT * FROM rebate_tradecomm WHERE CloseTime > :date")
    sql_results = db.execute(sql, {'date': expect_time})
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results
    
@app.get("/profit")
async def profit_record(db: Session= Depends(pure_sql), before_day: int = 7):
    time_delta = timedelta(days=before_day)
    expect_time = (datetime.now() - time_delta).strftime("%Y-%m-%d %H:%M:%S")
    sql = text("SELECT * FROM rebate_tradecomm WHERE CloseTime > :date")
    sql_results = db.execute(sql, {'date': expect_time})
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results
    
@app.post("/mt_total_comm")
async def mt_total_comm(db: Session= Depends(pure_sql), mtacc: str = '0',mtserver: str = '0'):
    #mt5_profit_sql = 
    sql = text("SELECT Mt4Account, Rebate_MtAccount, SUM(SumComm) AS Total_Comm, SUM(Profit) AS Total_Profit, SUM(m_Storage) AS Total_Swap FROM rebate_tradecomm WHERE rebate_tradecomm.Mt4Account = :mtacc AND rebate_tradecomm.MTServer = :mtserver GROUP BY Mt4Account, Rebate_MtAccount;")
    sql_results = db.execute(sql, {'mtacc': mtacc, 'mtserver': mtserver})
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@app.get("/rc_task_1")
async def rc_task_1(db: Session= Depends(pure_sql)):
    sql = text("SELECT t.Login,  mt.mt_group, SUM(t.Profit) AS Total_Profit, SUM(t.`Storage`) AS Total_Storage ,SUM(t.Commission) AS Total_ECN_Comm , SUM(Total_Profit + Total_Storage + Total_ECN_Comm) AS Real_Total_Profit FROM traderecord AS t LEFT JOIN mt_accounts AS mt ON t.Login = mt.mt_account  GROUP BY t.Login, mt.mt_group")
    sql_results = db.execute(sql)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@app.get("/rc_task_2")
async def rc_task_2(db: Session= Depends(pure_sql)):
    sql = text("SELECT t.Login,  mt.mt_group, SUM(t.Profit) AS Total_Profit, SUM(t.`Storage`) AS Total_Storage ,SUM(t.Commission) AS Total_ECN_Commissions FROM traderecord_mt5 AS t LEFT JOIN mt_accounts AS mt ON t.Login = mt.mt_account  GROUP BY t.Login, mt.mt_group")
    sql_results = db.execute(sql)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

# @app.get("/rc_task_3")
# async def rc_task_3(db: Session= Depends(pure_sql)):
#     sql = text("SELECT Mt4Account, MTServer, SUM(SumComm) AS Total_Comm FROM rebate_tradecomm GROUP BY Mt4Account, MTServer")
#     sql_results = db.execute(sql)
#     results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
#     return results

# @app.get("/rc_task_4")
# async def rc_task_4(db: Session= Depends(pure_sql)):
#     sql = text("SELECT f.mt_account, f.mt_server, SUM(f.deposit_dollar) AS Total_Deposit, SUM(f.withdraw_dollar) AS Total_Withdraw, SUM(f.adjust_dollar) AS Total_Adjust FROM ta_finance_records AS f WHERE f.fund_type LIKE '%DWDeposit%' OR f.fund_type LIKE '%DWWithdraw%' GROUP BY f.mt_account, f.mt_server")
#     sql_results = db.execute(sql)
#     results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
#     return results

@app.get("/mt4_total_summary")
async def mt4_total_summary(db: Session= Depends(pure_sql)):
    sql = text("SELECT t.Login,  mt.mt_group, (SUM(t.Profit) + SUM(t.`Storage`) + SUM(t.Commission)) AS Real_Total_Profit FROM traderecord AS t LEFT JOIN mt_accounts AS mt ON t.Login = mt.mt_account LEFT JOIN ta_finance_records AS mtds ON t.Login = mtds.mt_account  GROUP BY t.Login, mt.mt_group;")
    sql_results = db.execute(sql)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@app.get("/mt5_total_summary")
async def mt5_total_summary(db: Session= Depends(pure_sql)):
    sql = text("SELECT t.Login,  mt.mt_group, (SUM(t.Profit) + SUM(t.`Storage`) + SUM(t.Commission)) AS Real_Total_Profit FROM traderecord AS t LEFT JOIN mt_accounts AS mt ON t.Login = mt.mt_account GROUP BY t.Login, mt.mt_group;")
    sql_results = db.execute(sql)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@app.get("/test_summary")
async def test_summary(db: Session= Depends(pure_sql)):
    sql = await text("SELECT t.Login,  mt.mt_group, (SUM(t.Profit) + SUM(t.`Storage`) + SUM(t.Commission)) AS Real_Total_Profit, SUM(mtds.deposit_dollar) AS Total_MTDS FROM traderecord AS t LEFT JOIN mt_accounts AS mt ON t.Login = mt.mt_account LEFT JOIN ta_finance_records AS mtds ON t.Login = mtds.mt_account WHERE mtds.order_number LIKE '%MTDS%' GROUP BY t.Login, mt.mt_group;")
    sql_results = db.execute(sql)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results



    
    