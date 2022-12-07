from fastapi import Depends, APIRouter
from datetime import datetime, timedelta
from database import pure_session
import json
from datetime import datetime, timedelta
from decimal import *
from sqlalchemy.orm import Session
from sqlalchemy import text

router = APIRouter()

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
    


@router.post("/mt_total_comm", tags=["risk_control"])
async def mt_total_comm(db: Session= Depends(pure_sql), mtacc: str = '0',mtserver: str = '0'):
    #mt5_profit_sql = 
    sql = text("SELECT Mt4Account, Rebate_MtAccount, SUM(SumComm) AS Total_Comm, SUM(Profit) AS Total_Profit, SUM(m_Storage) AS Total_Swap FROM rebate_tradecomm WHERE rebate_tradecomm.Mt4Account = :mtacc AND rebate_tradecomm.MTServer = :mtserver GROUP BY Mt4Account, Rebate_MtAccount;")
    sql_results = db.execute(sql, {'mtacc': mtacc, 'mtserver': mtserver})
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@router.get("/mt4_total_summary", tags=["risk_control"])
async def mt4_total_summary(db: Session= Depends(pure_sql)):
    sql = text("SELECT mt.mt_account, mt.mt_group, mtds.Total_Deposit, tfds.Total_TFDS, t.Real_Total_Profit FROM mt_accounts AS mt LEFT JOIN (SELECT Login, (SUM(Profit) + SUM(`Storage`) + SUM(Commission)) AS Real_Total_Profit FROM traderecord GROUP BY Login) AS t ON t.Login = mt.mt_account LEFT JOIN (SELECT mt_account, SUM(deposit_dollar) AS Total_Deposit FROM ta_finance_records WHERE mt_server LIKE '%41%' GROUP BY mt_account) AS mtds ON mtds.mt_account = mt.mt_account LEFT JOIN (SELECT to_account, SUM(amount) AS Total_TFDS FROM ta_transfer_records WHERE to_mt_server LIKE '%41%' GROUP BY to_account) AS tfds on tfds.to_account = mt.mt_account WHERE mt.mt_group NOT LIKE 'T_%' AND mt.mt_server LIKE '%41%';")
    sql_results = db.execute(sql)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@router.get("/mt5_total_summary", tags=["risk_control"])
async def mt5_total_summary(db: Session= Depends(pure_sql)):
    sql = text("SELECT mt.mt_account, mt.mt_group, mtds.Total_Deposit, tfds.Total_TFDS, t.Real_Total_Profit FROM mt_accounts AS mt LEFT JOIN (SELECT Login, (SUM(Profit) + SUM(`Storage`) + SUM(Commission)) AS Real_Total_Profit FROM traderecord_mt5 GROUP BY Login) AS t ON t.Login = mt.mt_account LEFT JOIN (SELECT mt_account, SUM(deposit_dollar) AS Total_Deposit FROM ta_finance_records WHERE mt_server LIKE '%51%' GROUP BY mt_account) AS mtds ON mtds.mt_account = mt.mt_account LEFT JOIN (SELECT to_account, SUM(amount) AS Total_TFDS FROM ta_transfer_records WHERE to_mt_server LIKE '%51%' GROUP BY to_account) AS tfds ON tfds.to_account = mt.mt_account WHERE mt.mt_group NOT LIKE 'real\T_%' AND mt.mt_group NOT LIKE 'demo%' AND mt.mt_server LIKE '%51%';")
    sql_results = db.execute(sql)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@router.get("/rc_task_1", tags=["risk_control"])
async def rc_task_1(db: Session= Depends(pure_sql)):
    sql = text("SELECT t.Login,  mt.mt_group, SUM(t.Profit) AS Total_Profit, SUM(t.`Storage`) AS Total_Storage ,SUM(t.Commission) AS Total_ECN_Comm , SUM(Total_Profit + Total_Storage + Total_ECN_Comm) AS Real_Total_Profit FROM traderecord AS t LEFT JOIN mt_accounts AS mt ON t.Login = mt.mt_account  GROUP BY t.Login, mt.mt_group")
    sql_results = db.execute(sql)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results

@router.get("/rc_task_2", tags=["risk_control"])
async def rc_task_2(db: Session= Depends(pure_sql)):
    sql = text("SELECT t.Login,  mt.mt_group, SUM(t.Profit) AS Total_Profit, SUM(t.`Storage`) AS Total_Storage ,SUM(t.Commission) AS Total_ECN_Commissions FROM traderecord_mt5 AS t LEFT JOIN mt_accounts AS mt ON t.Login = mt.mt_account  GROUP BY t.Login, mt.mt_group")
    sql_results = db.execute(sql)
    results = json.loads(json.dumps([dict(r) for r in sql_results], cls=JsonEncoder))
    return results