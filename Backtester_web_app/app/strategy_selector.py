#modules to enable output of print statements on web app
import sys
import io
#modules for the strategies
import backtrader as bt
from bband_ema_strategy import BbandEma
from bband_rsi_strategy import BbandRsi
from ema_rsi_strategy import EmaRsi
from rsi_sma_strategy import RsiSma
from RSI_strategy1 import RsiStrategy
from simple_ema_strategy import EmaStrategy
from sma_close_price_strategy import SmaCloseprice
#Librarie to prepare data
import os
import pandas as pd
import polars as pl
from datetime import datetime
from sqlalchemy import create_engine, text, URL
from dotenv import load_dotenv
from data import stock_data_api, Db_Repo
load_dotenv()

#general function to get data
def wrangle(self, ticker, start_date, end_date):
        #setup conection to db
        engine= create_engine(f"duckdb:///{os.environ.get('DB_NAME')}")
        with engine.connect() as conn:
            #check if table exists
            result= conn.execute(text(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{ticker}'"))
            table_name= result.fetchone()
        if table_name is not None:
            #instantiate 'sqlrepo' class from data.py library
            repo= Db_Repo(uri=f"duckdb:///{os.environ.get('DB_NAME')}")
            #load data from table
            df= repo.read_table(ticker)
            #search through dataframe to get data between 'start_date' and 'end_date'
            df= df.filter(pl.col('Date').is_between(datetime.strptime(start_date, '%Y-%m-%d'), datetime.strptime(end_date, '%Y-%m-%d')))
            #gets fresh data from api if specific range of data is not available from the database
            if (df.is_empty()) or df['Date'].max() != (datetime.strptime(end_date, '%Y-%m-%d').date()):
                api= stock_data_api(ticker)
                data= api.get_data_from_api()
                repo.insert_data(table_name=ticker, records=data)
                #load data from table
                df= repo.read_table(ticker)
                #search through dataframe to get data between 'start_date' and 'end_date'
                df= df.filter(pl.col('Date').is_between(datetime.strptime(start_date, '%Y-%m-%d'), datetime.strptime(end_date, '%Y-%m-%d')))
            else:
                df= df
        else:
            #instantiate 'api_data' class from data.py library
            api= stock_data_api(ticker)
            data= api.get_data_from_api()
            #instantiate 'sqlrepo' class from data.py library
            repo= Db_Repo(uri=f"duckdb:///{os.environ.get('DB_NAME')}")
            #setup connection to execute and commit changes to the db based on the below query
            with engine.connect() as conn:
                conn.execute(text(f'Drop Table If Exists "{ticker}"'))
                conn.commit()
            #insert data into database
            repo.insert_data(table_name=ticker, records=data)
            #load data from table
            df=repo.read_table(ticker)
            #search through dataframe to get data between 'start_date' and 'end_date'
            df= df.filter(pl.col('Date').is_between(datetime.strptime(start_date, '%Y-%m-%d'), datetime.strptime(end_date, '%Y-%m-%d')))
        return df

        
def ema_rsi_strategy(ticker, start_date, end_date):
    df= wrangle(ticker, start_date, end_date)
    df= df.to_pandas()
    df.set_index('Date', inplace=True)
    df= df.sort_values(by='Date', ascending=True)
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
    df= df.to_pandas()
    df.set_index('Date', inplace=True)
    df= df.sort_values(by='Date', ascending=True)
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
    df= df.to_pandas()
    df.set_index('Date', inplace=True)
    df= df.sort_values(by='Date', ascending=True)
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
    df= df.to_pandas()
    df.set_index('Date', inplace=True)
    df= df.sort_values(by='Date', ascending=True)
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
    df= df.to_pandas()
    df.set_index('Date', inplace=True)
    df= df.sort_values(by='Date', ascending=True)
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
    df= df.to_pandas()
    df.set_index('Date', inplace=True)
    df= df.sort_values(by='Date', ascending=True)
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
    df= df.to_pandas()
    df.set_index('Date', inplace=True)
    df= df.sort_values(by='Date', ascending=True)
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
