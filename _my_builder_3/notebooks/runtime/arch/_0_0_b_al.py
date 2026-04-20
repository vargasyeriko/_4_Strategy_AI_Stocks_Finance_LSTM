import pandas as pd
import glob
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from _fns import main_stock_table_fetched,fetch_dividend_analysis
# Here build 
# 1 - every time you run it check price in last month and update if necessary 
# 2 - new stocks are added ... 

##################################### GET UPDATED stock list and start date
l_stocks_updt = fetch_fields()
d_start_date = '2022-07-01'
print('\n->', len(l_stocks_updt),f'Stocks being fetched from {d_start_date} till today') 
####################################################### Prices

# writes fetched table
main_stock_table_fetched(l_stocks_updt,d_start_date)    
              
########################################################## dividends

# writes fetched table
fetch_dividend_analysis(l_stocks_updt, d_start_date)

############################################################### END