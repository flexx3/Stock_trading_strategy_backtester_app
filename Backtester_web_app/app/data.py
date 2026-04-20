import requests
import pandas as pd
import polars as pl
import duckdb
from sqlalchemy import create_engine
import numpy as np
import os
from dotenv import load_dotenv
load_dotenv()

class stock_data_api:
    #setup init variables
    def __init__(self, ticker, api_key= os.environ.get('API_KEY')):
        self.ticker= ticker
        self.api_key= api_key
    #load data from api
    def get_data_from_api(self):
        #extract data from api
        url = f'https://api.twelvedata.com/time_series?symbol={self.ticker}&interval=1day&outputsize=5000&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        #A load and transform data in a pandas dataframe with the following steps
        df= pd.DataFrame().from_dict(data['values']) #1 load the specific json key
        #rename 'datetime' column to 'date'
        df.rename(columns={'datetime':'date'}, inplace=True)
        #capitalize first letter of all column names
        column_list= [column.capitalize() for column in df.columns.to_list()]
        df.columns= column_list
        #set 'date' column as index
        df.set_index('Date', inplace=True)
        #B load pandas dataframe into a polars dataframe with the following steps
        df2= pl.from_pandas(df, include_index=True)
        #convert columns to their appropriate datatypes
        df3= df2.with_columns(
            pl.col('Date').cast(pl.Date),
            pl.col('Open').cast(pl.Float64),
            pl.col('High').cast(pl.Float64),
            pl.col('Low').cast(pl.Float64),
            pl.col('Close').cast(pl.Float64),
            pl.col('Volume').cast(pl.Float64)
        )
        return df3
            
#load into a db
class Db_Repo:
    
    def __init__(self, uri):
        self.uri = uri
        
    #function to insert collected data from polars into a database
    def insert_data(self, table_name, records):
        #create connection to database using sqlalchemy
        conn = create_engine(self.uri)
        n_transactions = records.write_database(table_name=table_name, connection=conn.connect(), if_table_exists='replace')
        return(f'No of transactons: {n_transactions}')
        
    #function to read database data from a dataframe object
    def read_table(self, table_name):
        #create connection to database using sqlalchemy
        conn = create_engine(self.uri)
        #sql query to read data from database
        query = f"""
        SELECT * FROM '{table_name}'
        """
        #specify index column while reading the data into a dataframe
        df = pl.read_database(query, connection=conn.connect())
        #set to datetime index
        #df.index = pd.to_datetime(df.index)
        return df
