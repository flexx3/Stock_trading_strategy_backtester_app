import backtrader as bt

#create strategy template
class BbandRsi(bt.Strategy):
    params = (dict(rsi_periods= 7, period= 20, devfactor= 2))
    
    
    def __init__(self):
        self.close_price = self.datas[0].close
        
        #keep track of pending orders
        self.order = None
        self.price = None
        self.comm = None
        
        #setup rsi indicator
        self.rsi = bt.indicators.RSI(self.datas[0], period= self.p.rsi_periods)
        
        #setup bollingerbands indicator
        self.b_bands = bt.ind.BollingerBands(self.datas[0], period= self.p.period, devfactor= self.p.devfactor)
        
        #setup bband buy/sell signals
        self.bband_buy_signal = bt.ind.CrossUp(self.datas[0], self.b_bands.lines.mid)
        self.bband_sell_signal = bt.ind.CrossDown(self.datas[0], self.b_bands.lines.mid)
        
        
    def log(self, txt):
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
            if (self.rsi>20) and (self.rsi>60) and (self.bband_buy_signal):
                #buy order
                self.log(f'BUY CREATED --- CASH : {self.broker.getcash():.2f}, OPEN : {self.data_open[0]}, CLOSE : {self.data_close[0]}')
                self.buy()

        else:
            if (self.rsi<80) and (self.rsi<60) and (self.bband_sell_signal):
                self.log(f'SELL CREATED --- SIZE : {self.position.size}')
                self.sell(size= self.position.size)
        
