#modules to enable output of print statements on web app
import sys
import io
#modules for data processing
import pandas as pd
import sqlite3
from data import stock_data_api, Sqlrepo

#modules for the strategies
import backtrader as bt
from bband_ema_strategy import BbandEma
from bband_rsi_strategy import BbandRsi
from ema_rsi_strategy import EmaRsi
from rsi_sma_strategy import RsiSma
from RSI_strategy1 import RsiStrategy
from simple_ema_strategy import EmaStrategy
from sma_close_price_strategy import SmaCloseprice

#function to get data
def wrangle(ticker, start_date, end_date, use_new_data= True):
    #establish database connection
    connection= sqlite3.connect(database= 'yfstockdata.sqlite', check_same_thread= False)
    api= stock_data_api()
    repo= Sqlrepo(connection= connection)
    if (use_new_data):
        api_data = api.get_data(ticker= ticker)
        repo.insert_data(records= api_data, table_name= ticker, if_exists= 'replace')
    data= repo.read_table(ticker)
    df= data.loc[start_date:end_date]
    if df.shape[0]== 0:
        raise Exception(f"""oops! wrong date range, data only available between 
                        {data.index[0].strftime('%Y-%m-%d')} and {data.index[-1].strftime('%Y-%m-%d')}""")
    return df

        
def ema_rsi_strategy(ticker, start_date, end_date):
    df= wrangle(ticker, start_date, end_date)
    data= bt.feeds.PandasData(dataname= df)
    #instantiate cerebro
    cerebro= bt.Cerebro()
    #add strategy
    cerebro.addstrategy(EmaRsi)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000)
    cerebro.broker.setcommission(commission= 0.001)
    cerebro.addobserver(bt.observers.Value)
    # Redirect stdout to capture the print statements
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    print(f"---Starting portfolio value-----: {cerebro.broker.getvalue()}")
    cerebro.run()
    print(f"---Final portfolio value-----: {cerebro.broker.getvalue()}")
    # Reset stdout
    sys.stdout = old_stdout
    # Get the captured output
    output = new_stdout.getvalue()
    
    return output
    
def bband_ema_strategy(ticker, start_date, end_date):
    df= wrangle(ticker, start_date, end_date)
    data= bt.feeds.PandasData(dataname= df)
    #instantiate cerebro
    cerebro= bt.Cerebro()
    #add strategy
    cerebro.addstrategy(BbandEma)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000)
    cerebro.broker.setcommission(commission= 0.001)
    cerebro.addobserver(bt.observers.Value)
    # Redirect stdout to capture the print statements
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    print(f"---Starting portfolio value-----: {cerebro.broker.getvalue()}")
    cerebro.run()
    print(f"---Final portfolio value-----: {cerebro.broker.getvalue()}")
    # Reset stdout
    sys.stdout = old_stdout
    # Get the captured output
    output = new_stdout.getvalue()
    
    return output

def bband_rsi_strategy(ticker, start_date, end_date):
    df= wrangle(ticker, start_date, end_date)
    data= bt.feeds.PandasData(dataname= df)
    #instantiate cerebro
    cerebro= bt.Cerebro()
    #add strategy
    cerebro.addstrategy(BbandRsi)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000)
    cerebro.broker.setcommission(commission= 0.001)
    cerebro.addobserver(bt.observers.Value)
    # Redirect stdout to capture the print statements
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    print(f"---Starting portfolio value-----: {cerebro.broker.getvalue()}")
    cerebro.run()
    print(f"---Final portfolio value-----: {cerebro.broker.getvalue()}")
    # Reset stdout
    sys.stdout = old_stdout
    # Get the captured output
    output = new_stdout.getvalue()
    
    return output
    
def rsi_sma_strategy(ticker, start_date, end_date):
    df= wrangle(ticker, start_date, end_date)
    data= bt.feeds.PandasData(dataname= df)
    #instantiate cerebro
    cerebro= bt.Cerebro()
    #add strategy
    cerebro.addstrategy(RsiSma)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000)
    cerebro.broker.setcommission(commission= 0.001)
    cerebro.addobserver(bt.observers.Value)
    # Redirect stdout to capture the print statements
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    print(f"---Starting portfolio value-----: {cerebro.broker.getvalue()}")
    cerebro.run()
    print(f"---Final portfolio value-----: {cerebro.broker.getvalue()}")
    # Reset stdout
    sys.stdout = old_stdout
    # Get the captured output
    output = new_stdout.getvalue()
    
    return output

def rsi_strategy(ticker, start_date, end_date):
    df= wrangle(ticker, start_date, end_date)
    data= bt.feeds.PandasData(dataname= df)
    #instantiate cerebro
    cerebro= bt.Cerebro()
    #add strategy
    cerebro.addstrategy(RsiStrategy)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000)
    cerebro.broker.setcommission(commission= 0.001)
    cerebro.addobserver(bt.observers.Value)
    # Redirect stdout to capture the print statements
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    print(f"---Starting portfolio value-----: {cerebro.broker.getvalue()}")
    cerebro.run()
    print(f"---Final portfolio value-----: {cerebro.broker.getvalue()}")
    # Reset stdout
    sys.stdout = old_stdout
    # Get the captured output
    output = new_stdout.getvalue()
    
    return output
    
def ema_strategy(ticker, start_date, end_date):
    df= wrangle(ticker, start_date, end_date)
    data= bt.feeds.PandasData(dataname= df)
    #instantiate cerebro
    cerebro= bt.Cerebro()
    #add strategy
    cerebro.addstrategy(EmaStrategy)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000)
    cerebro.broker.setcommission(commission= 0.001)
    cerebro.addobserver(bt.observers.Value)
    # Redirect stdout to capture the print statements
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    print(f"---Starting portfolio value-----: {cerebro.broker.getvalue()}")
    cerebro.run()
    print(f"---Final portfolio value-----: {cerebro.broker.getvalue()}")
    # Reset stdout
    sys.stdout = old_stdout
    # Get the captured output
    output = new_stdout.getvalue()
    
    return output
    
def sma_closeprice_strategy(ticker, start_date, end_date):
    df= wrangle(ticker, start_date, end_date)
    data= bt.feeds.PandasData(dataname= df)
    #instantiate cerebro
    cerebro= bt.Cerebro()
    #add strategy
    cerebro.addstrategy(SmaCloseprice)
    cerebro.adddata(data)
    cerebro.broker.setcash(1000)
    cerebro.broker.setcommission(commission= 0.001)
    cerebro.addobserver(bt.observers.Value)
    # Redirect stdout to capture the print statements
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    print(f"---Starting portfolio value-----: {cerebro.broker.getvalue()}")
    cerebro.run()
    print(f"---Final portfolio value-----: {cerebro.broker.getvalue()}")
    # Reset stdout
    sys.stdout = old_stdout
    # Get the captured output
    output = new_stdout.getvalue()
    
    return output