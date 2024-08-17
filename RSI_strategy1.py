import backtrader as bt
import pandas as pd
import yfinance as yf
import datetime


#create strategy template
class RsiStrategy(bt.Strategy):
    params = dict(rsi_periods=7)
    
    def __init__(self):
        self.close_price = self.datas[0].close
        
        #keep track of pending orders
        self.order = None
        self.price = None
        self.comm = None
        
        #setup rsi indicator
        self.rsi = bt.indicators.RSI(self.datas[0], period= self.p.rsi_periods)
        

        
    def log(self, txt):
        dt = self.datas[0].datetime.date(0).isoformat()
        print(f"{dt}, {txt}")
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            #if order submitted/accepted by broker return nothing
            return
        #check if order is completed
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'Buy Order executed --- Price: {order.executed.price:.2f}, Cost: {order.executed.value}, Commission: {order.executed.comm}')
                self.price = order.executed.price
                self.commission = order.executed.comm
            
            elif order.issell():
                self.log(f'Sell Order executed --- Price: {order.executed.price:.2f}, Cost: {order.executed.value}, Commission: {order.executed.comm:.2f}')
            self.bar_executed = len(self)
                
        elif order.status in [order.Rejected, order.Canceled, order.Margin]:
            self.log('Order canceled/Margin/rejected')
            
        # Write down: no pending order
        self.order = None 
        
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(f'Operation result --- Gross: {trade.pnl:.2f}, NET: {trade.pnlcomm:.2f}')
            
        
    def next(self):
        self.log(f"Closing Price: {self.close_price[0]}")
        
        #check if an order is pending..if yes, we cannot send a second one
        if self.order:
            return
        
        #check if we are in the market
        if not self.position:
            if (self.rsi>20 and self.rsi>60):
                self.log(f'Buy Created: {self.close_price[0]}')
                self.order = self.buy()
                    
        else:
            
            if (self.rsi<80 and self.rsi<60):
                self.log(f'Sell Created: {self.close_price[0]}')
                #keep track of created order to avoid a second
                self.order = self.sell()