#import libraries for the visualization
from plotly.subplots import make_subplots
from plotly import graph_objects as go
import cufflinks as cf
from plotly.offline import iplot, init_notebook_mode
#instantiate and enable cufflinks in offline mode
#init_notebook_mode(connected= True)
cf.go_offline()
#Librarie to prepare data
import os
import pandas as pd
import polars as pl
from datetime import datetime
from sqlalchemy import create_engine, text, URL
from dotenv import load_dotenv
from data import stock_data_api, Db_Repo
load_dotenv()

class chart_selector:
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

    def plot_return(self, ticker, start_date, end_date):
        data= self.wrangle(ticker=ticker, start_date=start_date, end_date=end_date)
        data= data.to_pandas()
        data['Returns']= data['Close'].pct_change() *100
        #instantiate figure object
        figure= make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01, x_title='Date',row_heights=[800,600] )
        #add trace for returns
        figure.add_trace(go.Scatter(x= data['Date'], y= data['Returns'], mode= 'lines', name= 'Returns'), row=1, col=1)
        #add trace for volume
        figure.add_trace(go.Bar(x= data.index, y= data['Volume'], name= 'Volume'), row=2, col=1)
        #update layout 
        figure.update_layout(
            title= f'Returns and Volume over Time for {ticker} Stocks',
            yaxis_title= 'Returns',
            yaxis2_title= 'Volume'
        )
        return figure

    #function to plot price using quantfig library
    def plot_price_only(self, ticker, start_date, end_date):
        data= self.wrangle(ticker=ticker, start_date=start_date, end_date=end_date)
        data= data.to_pandas()
        data.set_index('Date', inplace=True)
        qf= cf.quant_figure.QuantFig(data, title= f"{ticker}'s stock price", legend= 'top', name= f'{ticker}')
        qf.add_rsi(periods= 7, rsi_upper= 80, rsi_lower= 20)
        qf.add_volume()
        return qf.iplot(asFigure=True)
    #observe simple moving averages
    def plot_sma_rsi(self, ticker, start_date, end_date):
        data= self.wrangle(ticker=ticker, start_date=start_date, end_date=end_date)
        data= data.to_pandas()
        data.set_index('Date', inplace=True)
        qf= cf.quant_figure.QuantFig(data, title= f"{ticker}'s stock price", legend= 'top', name= f'{ticker}')
        qf.add_sma(periods= 10, name= '10period sma')
        qf.add_sma(name= '20period sma', color= 'red')
        qf.add_rsi(periods= 7, rsi_upper= 80, rsi_lower= 20)
        qf.add_volume()
        return qf.iplot(asFigure=True)
    #visualize exponentialmovingaverages
    def plot_ema_rsi(self, ticker, start_date, end_date):
        data= self.wrangle(ticker=ticker, start_date=start_date, end_date=end_date)
        data= data.to_pandas()
        data.set_index('Date', inplace=True)
        qf= cf.quant_figure.QuantFig(data, title= f"{ticker}'s stock price", legend= 'top', name= f'{ticker}')
        qf.add_ema(periods=10, color= 'green', name= '10period ema')
        qf.add_ema(periods=20, color= 'red', name= '20period ema')
        qf.add_rsi(periods= 7, rsi_upper= 80, rsi_lower= 20)
        qf.add_volume()
        return qf.iplot(asFigure=True)
    #observe pricevolatility using bollinger
    def plot_bollinger(self, ticker, start_date, end_date):
        data= self.wrangle(ticker=ticker, start_date=start_date, end_date=end_date)
        data= data.to_pandas()
        data.set_index('Date', inplace=True)
        qf= cf.quant_figure.QuantFig(data, title= f"{ticker}'s stock price", legend= 'top', name= f'{ticker}')
        qf.add_bollinger_bands()
        qf.add_ema(periods=50, color= 'green', name= '10period ema')
        qf.add_volume()
        #qf.add_rsi(periods= 7, rsi_upper= 80, rsi_lower= 20)
        return qf.iplot(asFigure=True)
    #observe trend changes with macd
    def plot_macd_adx(self, ticker, start_date, end_date):
        data= self.wrangle(ticker=ticker, start_date=start_date, end_date=end_date)
        data= data.to_pandas()
        data.set_index('Date', inplace=True)
        qf= cf.quant_figure.QuantFig(data, title= f"{ticker}'s stock price", legend= 'top', name= f'{ticker}')
        qf.add_macd()
        qf.add_adx()
        qf.add_volume()
        #qf.add_rsi(periods= 7, rsi_upper= 80, rsi_lower= 20)
        return qf.iplot(asFigure=True)
    

