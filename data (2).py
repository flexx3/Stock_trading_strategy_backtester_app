import pandas as pd
import sqlite3
import yfinance as yf

class stock_data_api:
     
    #get data from yfinance 
    def get_data(self, ticker):
        data = yf.download(ticker, auto_adjust= True, progress= False)
        return data
            
class Sqlrepo:
    def __init__(self, connection):
        #setup connection to database
        self.connection= connection
     
    #function to insert collected data into a database
    def insert_data(self, table_name, records, if_exists):
        n_inserted = records.to_sql(name= table_name, con= self.connection, if_exists= if_exists)
        return{
            "transaction successful": True,
            "Number of records": n_inserted
        }
    
    #function to read database data from a dataframe object
    def read_table(self, table_name):
        #sql query to read data from database
        query = f"""
        SELECT * FROM {table_name}
        """
        #specify index column while reading the data into a dataframe
        df = pd.read_sql(query, con= self.connection, index_col= 'Date')
        #set to datetime index
        df.index = pd.to_datetime(df.index)
        return df