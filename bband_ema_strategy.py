import backtrader as bt

class BbandEma(bt.Strategy):
    params = (dict(period= 20, devfactor= 2, ema_period= 50))
    
    def __init__(self):

        #keep track of close price in the series
        self.data_close = self.datas[0].close
        self.data_open = self.datas[0].open

        #keep track of pending orders, buy/sell price, commision
        self.order = None
        self.price = None
        self.comm = None
        
        #add ema line indicator
        self.ema_line = bt.ind.EMA(self.datas[0], period= self.p.ema_period)

        #add bollinger bands indicator
        self.b_bands = bt.ind.BollingerBands(self.datas[0], period= self.p.period, devfactor= self.p.devfactor)
        
        #track buy/sell signals
        self.buy_signal = bt.ind.CrossUp(self.ema_line, self.b_bands.lines.mid)
        self.sell_signal = bt.ind.CrossDown(self.ema_line, self.b_bands.lines.mid)
        
        
     #set log
    def log(self, txt):
        '''logging function'''
        dt = self.datas[0].datetime.date(0).isoformat()
        print(f'{dt}, {txt}')
        
        
    def notify_order(self, order):
        #if order is submitted/accepted - no action required
        if order.status in [order.Submitted, order.Accepted]:
            return

        #report executed order
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f'BUY EXECUTED ---- PRICE : {order.executed.price:.2f}, Cost : {order.executed.value:.2f}, COMMISSION : {order.executed.comm:.2f}'
                )
                self.price = order.executed.price
                self.comm = order.executed.comm

            else:
                self.log(f'SELL EXECUTED ---- PRICE : {order.executed.price:.2f}, COST : {order.executed.value:.2f}, COMMISSION : {order.executed.comm:.2f}')

        #report failed order
        elif order.status in [order.Cancelled, order.Rejected, order.Margin]:
            self.log('Order Failed')

        #set no pending order
        self.order = None
        
    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log(
            f'OPERATION RESULT --- GROSS : {trade.pnl:.2f}, NET : {trade.pnlcomm:.2f}'
        ) 
        
    def next(self):
        if not self.position:
            if self.buy_signal:
                #buy order
                self.log(f'BUY CREATED --- CASH : {self.broker.getcash():.2f}, OPEN : {self.data_open[0]}, CLOSE : {self.data_close[0]}')
                self.buy()

        else:
            if self.sell_signal:
                self.log(f'SELL CREATED --- SIZE : {self.position.size}')
                self.sell(size= self.position.size)

        
        
        
        
        
        
        
        