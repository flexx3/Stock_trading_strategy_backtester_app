#!/usr/bin/env python
# coding: utf-8

# In[1]:


from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container


# In[2]:


#instantiate dash app
app = Dash(__name__,
           assets_folder = 'assets',
          external_stylesheets = [dbc.themes.BOOTSTRAP],
          title='Built by Flexxie', 
          meta_tags=[{'name': 'viewport',
                      'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.5, minimum-scale=0.5'}],)
server = app.server

# In[3]:


#instantiate app server
server = app.server


# In[4]:


#logo source
navbar_logo_src = "./assets/stock-icon.png"
sidebar_logo_src1 = "./assets/linkedin-logo.png"
sidebar_logo_src2 = "./assets/github-mark.png"

#inline styling for left-sidebar with a fixed height,width and distance from the top
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "76px",
    "left": 0,
    "bottom": 0,
    "overflow": "auto"    
}
app.layout = html.Div([
         #Navbar layout with an auto fixed height,width and bottom distance
        dbc.Navbar(dbc.Container(
    [
        dbc.Row([
            dbc.Col(html.Img(src = navbar_logo_src, height = '60px')),
            dbc.Col(dbc.NavbarBrand('BacktesterApp', className = 'ms-2')),
        ], align = 'center', className = 'g-0')
    ]
), color = 'dark', dark = True, fixed='top'),
 #left-sidebar layout embedding the inline styles   
dbc.Navbar(
    dbc.Container([
        dbc.Nav([
            dbc.NavItem(html.H4('Reach Me'), style = {'text-align':'center'}),
            dbc.NavItem(html.Hr()),
            dbc.NavItem(dbc.NavLink(html.Img(src = sidebar_logo_src2,
                                             style = {'height':'60px'}),href = 'https://github.com/flexx3'),
                        style = {'padding':'16px'}),
            dbc.NavItem(dbc.NavLink(html.Img(src = sidebar_logo_src1,
                                             style = {'height':'60px'}),
                                    href = 'https://www.linkedin.com/in/felix-obioma-nkwuzor-828a20215/'),
                        style = {'padding':'16px'}),
            dbc.NavItem(dbc.NavLink(html.Img(src = './assets/gmail-logo.png',
                                             style = {'height':'60px'}),href = 'https://felixobioma99@gmail.com'),
                        style = {'padding':'10px'}),
        ], vertical = True,
        navbar = True)
    ], fluid = True), style = SIDEBAR_STYLE, color = 'lightgrey', dark = False
),
 #main content area   
 html.Div(
     dbc.Container([
         dbc.Row([
             dbc.Col(html.Div([html.Label('Select stock ticker'),
            dcc.Dropdown(id = 'ticker-symbol',options = [
            {'label':'MSFT', 'value':'MSFT'},
            {'label':'AAPL', 'value':'AAPL'},
            {'label':'META', 'value':'META'},
            {'label':'AMZN', 'value':'AMZN'},
            {'label':'TSLA', 'value':'TSLA'},
            {'label':'GOOGL', 'value':'GOOGL'},
            {'label':'WMT', 'value':'WMT'},
            {'label':'NVDA', 'value':'NVDA'},
            {'label':'AMZN', 'value':'AMZN'},
            {'label':'ORCL', 'value':'ORCL'},
            {'label':'JMIA', 'value':'JMIA'},
            {'label':'IHS', 'value':'IHS'},     
             ],
                                  
               clearable = False ,value='AAPL' , style = {'border-radius':'50px', #rounded edge
                'background-color':'lightgrey'})])),
             dbc.Col(html.Div([html.Label('Input startDate'),dcc.Input(id = 'start-date', type='text',
            minLength=10, maxLength=10, value = '2023-01-01',
            placeholder = 'yyyy-mm-dd',style = {'border-radius':'50px', 'text-align':'center'})],
            style = {'text-align':'center'})),
             dbc.Col(html.Div([html.Label('Input endDate'),dcc.Input(id = 'end-date', type='text', minLength=10,maxLength=10,
              value='2023-12-31', placeholder = 'yyyy-mm-dd',style = {'border-radius':'50px', 'text-align':'center'})],
            style = {'text-align':'center'})),
             dbc.Col(html.Div([html.Label('click button after inputting dates'),
            dbc.Button('Submit',id='date-inputerbutton',n_clicks=0, style={'background-color':'black'})])),
             dbc.Col(html.Div([html.Label('Select chart'),
                dcc.Dropdown(id ='chart-selector', options = [
                 {'label':'candlestick', 'value':'candlestick'},
                 {'label':'sma', 'value':'sma'},
                 {'label':'ema', 'value':'ema'},
                 {'label':'bollingerbands', 'value':'bollinger'},
                 {'label':'log returns', 'value':'returns'},
             ], clearable = False, value='candlestick',
             style = {'border-radius':'50px',
                               'background-color':'lightgrey'})]),)
         ]),
         
         dbc.Row([
             dcc.Graph(id = 'output-chart', figure = {})
         ]),
         #prepare layout for selecting the trading strategies to backtest
         dbc.Row([
         html.Div([
        html.H5('Select trading strategies to backtest(Cash=1000, Commission=0.1%)'),
        dcc.Dropdown(id='backtester-dropdown', options=[
{'label':html.Pre('1. buy and hold when ema(50period) crosses above the middle bollinger\nsell when ema crosses below the middle bollinger.',
                 style={'marginTop':'20px'}),'value':'EmaBband'},
{'label':html.Pre('2. buy if closingprice is above the middle bolinger and rsi>20 and 60\nsell if closingprice is in reverse and rsi < 80 and 60.',
                 style={'marginTop':'20px'}), 'value':'BbandRsi'},
{'label':html.Pre('3. buy if shorter ema(10period) crosses above a longer ema(20period) and rsi(7period)>60\nsell if in reverse.',
                 style={'marginTop':'20px'}), 'value':'EmaRsi'},
{'label':html.Pre('4. buy if shorter sma(10period) crosses above a longer sma(20period) and rsi(7period)>60\nsell if in reverse.',
                 style={'marginTop':'20px'}), 'value':'RsiSma'},
{'label':html.Pre('5. buy if rsi(7periods) > 20 and 60\nsell if rsi < 80 and 60.',
                 style={'marginTop':'20px'}), 'value':'SimpleRsi'},
{'label':html.Pre('6. buy if shorter ema(10period) crosses above a longer ema(20period)\nsell if in reverse.',
                 style={'marginTop':'20px'}), 'value':'SimpleEma'},
{'label':html.Pre('7. buy if closingprice > sma(20period), sell if closingprice < sma.',
                  style={'marginTop':'20px'}), 'value':'SmaPrice'}
                 ])
             ], style={'text-align':'center'})
             
             
             
             
         ]),
         dbc.Row([
             html.Pre(id='backtester-output')
         ])
         
         #to avoid overlapping with side-bar and navbar
     ], fluid = True, style = {'width':'76%','margin-top':'76px'}),
     
     
 )
    
])


# In[5]:


#prepare data for upload
#import data library
from data import stock_data_api, Sqlrepo
import sqlite3
import pandas as pd
import numpy as np

#function to get data
def wrangle(ticker, start_date, end_date, use_new_data= True):
    
    #establish database connection
    connection= sqlite3.connect(database= 'yfstockdata.sqlite', check_same_thread= False)
    api= stock_data_api()
    repo= Sqlrepo(connection= connection)
    if use_new_data:
        api_data = api.get_data(ticker=ticker)
        repo.insert_data(records= api_data, table_name= ticker, if_exists= 'replace')
    data= repo.read_table(ticker)
    #sort values in ascending order
    data.sort_values(by= 'Date', inplace= True)
    df = data.loc[start_date:end_date]
    #calculate returns
    df['Returns']= np.log(df['Close']/df['Close'].shift(1))
    df.fillna(method= 'ffill', inplace= True)
    if df.shape[0]== 0:
        raise Exception(f"""oops! wrong date range, data only available between {df.index[0].strftime('%Y-%m-%d')} and {df.index[-1].strftime('%Y-%m-%d')}""")
    return df
           
    


# In[6]:


#callback to output the chart
#first import the charts module
from charts import chart_selector

@callback(
    Output(component_id='output-chart', component_property='figure'),
    Input(component_id='ticker-symbol', component_property='value'),
    Input(component_id='date-inputerbutton', component_property='n_clicks'),
    State(component_id='start-date', component_property='value'),
    State(component_id='end-date', component_property='value'),
    Input(component_id='chart-selector', component_property='value')
)

def display_chart(ticker, clicks, start_date, end_date, chart):
    #get data
    data = wrangle(ticker, start_date, end_date)
    if clicks is None:
        chart_data = None
    else:
        chart_data = data
    #instantiate charts
    charts_selector = chart_selector()
    if chart == 'candlestick':
        chart_output = charts_selector.plot_price_only(chart_data, ticker)
    elif chart == 'sma':
        chart_output = charts_selector.plot_sma_rsi(chart_data, ticker)
    elif chart == 'ema':
        chart_output = charts_selector.plot_ema_rsi(chart_data, ticker)
    elif chart == 'bollinger':
        chart_output = charts_selector.plot_bollinger(chart_data, ticker)
    elif chart == 'returns':
        chart_output = charts_selector.plot_return(chart_data, ticker)
        
    return chart_output
    


# In[7]:


#callback to output the backtester results
#import the backtester selector module
import strategy_selector as ss
@callback(
    Output(component_id='backtester-output', component_property='children'),
    Input(component_id='ticker-symbol', component_property='value'),
    Input(component_id='date-inputerbutton', component_property='n_clicks'),
    State(component_id='start-date', component_property='value'),
    State(component_id='end-date', component_property='value'),
    Input(component_id='backtester-dropdown', component_property='value')
)

def run_backtester(ticker, clicks, start_date, end_date, strategy):
    if clicks is None:
        start_date = None
        end_date = None
    else:
        start_date = start_date
        end_date = end_date
    #run the backtester algorithm
    if strategy == 'EmaBband':
        return ss.bband_ema_strategy(ticker, start_date, end_date)
    elif strategy == 'BbandRsi':
        return ss.bband_rsi_strategy(ticker, start_date, end_date)
    elif strategy == 'EmaRsi':
        return ss.ema_rsi_strategy(ticker, start_date, end_date)
    elif strategy == 'RsiSma':
        return ss.rsi_sma_strategy(ticker, start_date, end_date)
    elif strategy == 'SimpleRsi':
        return ss.rsi_strategy(ticker, start_date, end_date)
    elif strategy == 'SimpleEma':
        return ss.ema_strategy(ticker, start_date, end_date)
    elif strategy == 'SmaPrice':
        return ss.sma_closeprice_strategy(ticker, start_date, end_date)
    
        


# In[8]:


#run app
if __name__ == '__main__':
    app.run_server(debug=False)


# In[ ]:




