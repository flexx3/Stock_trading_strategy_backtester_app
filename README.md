This backtester app project is in three phases; data phase, charts/backtester phase, web app phase.
For the data phase, the data.py module consists of an ETL process written using OOP methodologies.
Specific stock data from the user is gotten from  twelvedata api, cleaned and organised,
stored into a duckdb database for running analysis, charts and backtests using requests, pandas, polars, datetime, sqlalchemy/duckdb, etc.
charts.py consist of code for outputting specific visuals for specific stock data based on user preference.
strategy_selector.py consists of code enabling the user to select and run bactests for specific stocks. it ouputs results for all seven strategies(written using backtrader) in this project.
charts.py and strategy_selector both imports the data.py module to access data.
The entire arrangement is now put together in plotly dash web app(Backtester_dash_app) with its corresponding web pages.
Code was optimized to reduce unnecessary api calls. The entire credentials (api keys, database info) needed for this project is covered in a .env file.
Functional app deployed on render. The About page contains all you need to know to use the app well.
Periodical maintainance will be done on the app due to limited limit alloted to host the database for this project by the cloud platform.
Thanks so much for your time. 
 
