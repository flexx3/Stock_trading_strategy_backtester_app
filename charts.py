#import libraries for the visualization
import plotly.express as px
from plotly.subplots import make_subplots
from plotly import graph_objects as go
import cufflinks as cf

class chart_selector:

    def plot_return(self, data, ticker):
        #instantiate figure object
        figure= make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.01, x_title='Date',row_heights=[800,600] )

        #add trace for returns
        figure.add_trace(go.Scatter(x= data.index, y= data['Returns'], mode= 'lines', name= 'Returns'), row=1, col=1)

        #add trace for volume
        figure.add_trace(go.Bar(x= data.index, y= data['Volume'], name= 'Volume'), row=2, col=1)

        #update layout 
        figure.update_layout(
            title= f'Returns and Volume over Time for {ticker} Stocks',
            yaxis_title= 'Returns',
            yaxis2_title= 'Volume'
        )

        return figure

    def plot_price_only(self, data, ticker):
        qf= cf.quant_figure.QuantFig(data,title= f"{ticker}'s stock price", legend= 'top', name= f'{ticker}')
        qf.add_volume()
        qf.add_rsi(periods= 7, rsi_upper= 80, rsi_lower= 20)
        figure = qf.iplot(asFigure=True)
        return figure


    def plot_sma_rsi(self, data, ticker):
        qf= cf.quant_figure.QuantFig(data,title= f"{ticker}'s stock price", legend= 'top', name= f'{ticker}')
        qf.add_volume()
        qf.add_sma(periods= 10, name= '10period sma', color='yellow')
        qf.add_sma(name= '20period sma', color='green')
        qf.add_rsi(periods= 7, rsi_upper= 80, rsi_lower= 20)
        figure = qf.iplot(asFigure=True)
        return figure

    def plot_ema_rsi(self, data, ticker):
        qf= cf.quant_figure.QuantFig(data,title= f"{ticker}'s stock price", legend= 'top', name= f'{ticker}')
        qf.add_volume()
        qf.add_ema(periods=10,  name= '10period ema', color='yellow')
        qf.add_ema(periods=20,  name= '20period ema', color='green')
        qf.add_rsi(periods= 7, rsi_upper= 80, rsi_lower= 20)
        figure = qf.iplot(asFigure=True)
        return figure

    def plot_bollinger(self, data, ticker):
        qf= cf.quant_figure.QuantFig(data,title= f"{ticker}'s stock price", legend= 'top', name= f'{ticker}')
        qf.add_volume()
        qf.add_bollinger_bands()
        qf.add_ema(periods=50, name= '10period ema', color='gold')
        qf.add_rsi(periods= 7, rsi_upper= 80, rsi_lower= 20)
        figure = qf.iplot(asFigure=True)
        return figure

