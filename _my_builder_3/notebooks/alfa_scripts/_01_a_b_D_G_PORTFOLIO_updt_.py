# ############ ASK PROGRAM -> modify so first time is run , does not let the user ask until is ran ,
# # or be like last update was made this date, do you wish to update before ...
########################################################################
import os
import ast
import glob
import shutil
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timedelta
######################################################################## VARIABLES & FUNCTIONS
#
from _fns import sum_units_sold_by_stock_bought,sum_units_sold_by_stock_sold
from _fns import sum_buy_sell_ordered,concat_pkl_to_df,get_unique_stocks
from _fns import main_stock_table_fetched,fetch_dividend_analysis
from _fns import calculate_and_add_dividends, analyze_dates
from _fns import fetch_stock_price_on_date_close
#
from _0_0_all_stocks_ import df_ce_all_hist,d_start_date,total_inv,formatted_date_time
from _0_0_all_stocks_ import data_to_append_df_d,data_to_append_df_g ,df_ce_all_hist
from _0_0_all_stocks_ import portfolio_labels_d,portfolio_labels_g , stock_list_ce
from _0_0_all_stocks_ import portfolio_percentages_d,portfolio_percentages_g
#
exec(open(f"_0_b_fns_PORTFOLIO_updt.py",encoding="utf-8").read())
#
################################################################### PY PROGRAM NAMES
name_updt_ledger_till_ce = '_11_a_LEDGER_till_CashExcess_'
name_updt_no_ledger_ce   = '_11_a_NO_LEDGER_till_CashExcess_'
name_1_a_Cash_Excess_calc = '_1_a_CASH_Excess_calculation'
# UNITS
df_name_units_updt = f'_df_0_init_UNITS'
df_add_name_st_exch = '_df_add_1_up_to_date_UNITS'
### DATE
start_date_reset = d_start_date
##########################################################################  FETCH
hist_df_0 = pd.concat([data_to_append_df_g,data_to_append_df_d], ignore_index=True)
df_add = concat_pkl_to_df(hist_df_0, directory="_2_tables_add/")

# Get initial UNIQUE STOCK list 
l_stocks_updt = get_unique_stocks(portfolio_labels_g,portfolio_labels_d,stock_list_ce,df_add)
# ########## FEtCH !!
# Creating a DataFrame from the list
df_all_st = pd.DataFrame(l_stocks_updt, columns=['Stock'])
df_all_st.to_pickle(f'_1_fetch/stock_list/_updt_list_{formatted_date_time}.pkl')
############ new Stocks -> FEtch
update_stock_list()

# Check if the file exists
if not os.path.exists( '_1_fetch/_0_fetched_stock_data_prices.pkl'):
    # UPDATE STOCKS
    main_stock_table_fetched(l_stocks_updt, d_start_date)
   
if not os.path.exists('_1_fetch/_1_fetched_stock_dividend_percentages.pkl'):
    # UPDATE DIVS
    fetch_dividend_analysis(l_stocks_updt, d_start_date)

# ########## FEtCH !! check if days more days has passed or more stocks have been added
df_close = master_fetch_check(l_stocks_updt,d_start_date)

##########################################################################

######################################## choose risk prifile
risk_profile = pick_profile()
allocations = generate_portfolio_allocations(total_inv, risk_profile)
#
## Assign investments based on allocations
#
initial_investment_G = allocations['Growth']
print(f"\nINIT Growth $ :\t {initial_investment_G}")
initial_investment_D = allocations['Defensive']
print(f"\nINIT Defensive $:\t {initial_investment_D}")
#
######################################## reset folders -> Directories list
directories = ["_1_tables", "_20_add_cash", 
               "_21_add_ledger_sell", "_22_add_ledger_buy"]
confirm_and_execute(directories)
######################################## build portfolio
#exec(open(f"_0_D_PORTFOLIO_hist_.py",encoding="utf-8").read()) 
hist_df_d,df_d,cash_start_value_d= _PORT_DEF_get()
## Growght
hist_df_g,df_g,cash_start_value_g= _PORT_GRO_get()

#exec(open(f"_0_G_PORTFOLIO_hist_.py",encoding="utf-8").read()) 
####################################################################################################################################################
# # # HIST -> DATA
# CONCAT ALL HIST TO BE PROCESSED 

hist_df_0 = pd.concat([hist_df_d,hist_df_g], ignore_index=True)
df_add = concat_pkl_to_df(hist_df_0, directory="_2_tables_add/")
df_add = df_add.sort_values(by='DateTrans').copy().reset_index(drop=True)# SORT by dates
############################################################################

# ############################################################################
# ############################################################################
d_start_date =start_date_reset
df_g = df_g.iloc[:-2]
df_d = df_d.iloc[:-2]

df = pd.concat([df_d,df_g], ignore_index=True) # concat

# ############################################################################
# ############################################################################
# ADD NEW stocks NAMES to master table from history and rite master table
#
# Step 1: Prepare 'df_add' by converting strings in 'exchange_stocks' to lists and converting 'DateTrans' to datetime
df_add['exchange_stocks'] = df_add['exchange_stocks'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
df_add['DateTrans'] = pd.to_datetime(df_add['DateTrans'])

# Step 2: Extract unique stocks from 'exchange_stocks'
unique_exchange_stocks = set()
df_add['exchange_stocks'].apply(lambda x: unique_exchange_stocks.update(x))

# Step 3: Identify stocks not in 'df["Stock"]' ################################### dff ref first time
stocks_set = set(df['Stock'])
stocks_not_in_df = unique_exchange_stocks.difference(stocks_set)

# Step 4: Find the earliest transaction date for each stock not in 'df'
earliest_dates_for_new_stocks = {stock: datetime.max for stock in stocks_not_in_df}
for _, row in df_add.iterrows():
    for stock in row['exchange_stocks']:
        if stock in stocks_not_in_df and row['DateTrans'] < earliest_dates_for_new_stocks[stock]:
            earliest_dates_for_new_stocks[stock] = row['DateTrans']


# Step 5: Add missing stocks to 'df' with 'hold_units_at_init' set to 0 and formatted 'StartDate'
for stock in stocks_not_in_df:
    earliest_date_str = earliest_dates_for_new_stocks[stock].strftime('%Y-%m-%d')  # Format date as string
    new_row = pd.DataFrame({
    'Stock': [stock],  # Assuming 'stock' and 'earliest_date_str' are defined variables
    'Price Bought': [0],
    'Latest Price': [0],
    'Invested Amount (AUD)': [0],
    'Transaction Fee (AUD)': [0],
    'Net Cash Value (AUD)': [0],
    'StartDate': [earliest_date_str],
    'Percentage': [0],
    'hold_units_at_init': [0]})

    # Concatenate the new row to the existing DataFrame
    df = pd.concat([df, new_row], ignore_index=True)


# Ensure 'StartDate' column exists in 'df' and is properly formatted
if 'StartDate' not in df.columns:
    df['StartDate'] = pd.NaT  # Initialize 'StartDate' column if it doesn't exist

    
########################################### EXPORT 0 UNITS 
#::: df_0_upft_units.pkl :::: UNITS INIT
df['hold_units_at_init_day_1']= df['hold_units_at_init']        ## JUST ADDED
df.to_pickle(f'_1_tables/_df_0_init_UNITS.pkl')

# df['hold_units_at_init_day_1']= df['hold_units_at_init']
# df.to_pickle(f'_1_tables/_df_01_init_INVESTMENT_UNITS_START_.pkl')


########################################### EXPORT 1 UNITS
#..._df_add_1_up_to_date_UNITS.pkl # ::::: CASH INIT


df_add.to_pickle(f'_1_tables/_df_add_1_up_to_date_UNITS.pkl')
print('\n_df_0 >>> df_master with up-to-date units balances written df_0  :') 
print('_df_1 >>> df_add    with ALL Exchange transactions written df_1  :') 



########################################### EXPORT 0 ::: CASH
#_df_cash_init_1_init_CASH.pkl # ::::: CASH INIT

cash_start_value = cash_start_value_d+cash_start_value_g

data = {
    'amount': cash_start_value,  # Scalar value
    'DateTrans': d_start_date,  # Scalar value
    'id_time_buy': f'INIT_CASH_Def_Gro_{d_start_date}',  # Scalar value
    'trans_type': 'cash_init',  # Scalar value
    'costs': 0  # Scalar value
}
# You can create an index as a list with a single element if there is only one row of data
index = [0]  # Single row DataFrame
df_cash_init = pd.DataFrame(data, index=index).sort_values(by='DateTrans').reset_index(drop=True)


df_cash_init.to_pickle(f'_20_add_cash/_df_cash_init_0_init_CASH.pkl') #cashete


########################################### EXPORT 1 ::: CASH LEDGER updt INITIALIZE
import pandas as pd

# Define the columns for the DataFrame
columns = {
    'amount': None,
    'DateTrans': None,
    'id_time_buy': None,
    'trans_type': None,
    'costs': None
}

# Initialize an empty DataFrame with these columns
df_cash_init_empty = pd.DataFrame(columns=columns.keys())

# Save the empty DataFrame to a .pkl file
df_cash_init_empty.to_pickle(f'_20_add_cash/_df_cash_init_1_empty_CASH.pkl') 

print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_' )
#print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_' )

