#import libraries
import backtrader as bt

#create strategy template
class RsiSma(bt.Strategy):
    params = (dict(rsi_periods= 7, sma_lower= 10, sma_higher= 20))
    
    
    def __init__(self):
        self.close_price = self.datas[0].close
        
        #keep track of pending orders
        self.order = None
        self.price = None
        self.comm = None
        
        #setup rsi indicator
        self.rsi = bt.indicators.RSI(self.datas[0], period= self.p.rsi_periods)
        #setup sma indicator
        self.sma_faster = bt.indicators.SMA(self.datas[0], period= self.p.sma_lower)
        self.sma_slower = bt.indicators.SMA(self.datas[0], period= self.p.sma_higher)
        
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

        self.log(f'OPERATION RESULT --- Gross: {trade.pnl:.2f}, Net: {trade.pnlcomm:.2f}')
        
    def next(self):
        # do nothing if an order is pending
        if self.order:
            return

        # check if there is already a position
        if not self.position:
            # buy condition
            if (self.rsi>60) and (self.sma_faster[0]>self.sma_slower[0]):
                self.log(f'BUY CREATED --- Price: {self.data_close[0]:.2f}')
                self.order = self.buy()
        else:
            # sell condition
            if (self.rsi<60) and (self.sma_faster[0]<self.sma_slower[0]):
                self.log(f'SELL CREATED --- Price: {self.data_close[0]:.2f}')
                self.order = self.sell()
        
        
        
        