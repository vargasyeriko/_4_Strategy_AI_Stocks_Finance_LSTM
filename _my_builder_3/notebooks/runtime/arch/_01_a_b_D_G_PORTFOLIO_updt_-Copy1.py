############ ASK PROGRAM -> modify so first time is run , does not let the user ask until is ran ,
# or be like last update was made this date, do you wish to update before ...
############################################################################
############################################################################ ASK
import os
import subprocess
from datetime import datetime
from datetime import datetime, timedelta
import pandas as pd
import shutil
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import glob



## Get the current date and time
now = datetime.now();formatted_date_time = now.strftime("%Y_%m_%d_h%Hm%M")

############################################################################ 
from _fns import sum_units_sold_by_stock_bought,sum_units_sold_by_stock_sold,sum_buy_sell_ordered
from _fns import main_stock_table_fetched,fetch_dividend_analysis

############################################################################
############################################################################
rsp_now = input('Did you make any changes in the previous month? <Enter:skip> <y:add_change>')
if rsp_now == 'y':
    #
    df= pd.read_pickle(f'_1_tables/_df_0_init_UNITS.pkl')
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("1. Add exchange stock \n\t\t\t *a) : stock to stock",
          "\n\t\t\t *b) : stock to cash\n\n2. Buy stock from Excess cash")
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")

    choice = input("\nEnter your choice (1 or 2): ")

    # EXCHANGE STOCK
    if choice == "1":
        #subprocess.run(['python',f"{direc}/_0_a1_PORTFOLIO_entry_updt_.py"], cwd=f'{direc}')
        exec(open(f"_0_a1_PORTFOLIO_entry_updt_.py",encoding="utf-8").read()) #paths

    # CASH ECSESS
    elif choice == "2":
        exec(open(f"_0_a2_PORTFOLIO_entry_updt_.py",encoding="utf-8").read()) 
    else:
        print("Invalid choice. Please enter 1 or 2.")
else:
    print('No CHANGES made ... CNTD ... \n')
############################################################################
############################################################################


############################################## RESET FOLDERS 
############################################################################

def archive_pkl_files(directories):
    for direc in directories:
        archive_path = os.path.join(direc, "archive")
        os.makedirs(archive_path, exist_ok=True)  # Create 'archive' if it doesn't exist
        
        # List all pkl files in the directory
        files = [f for f in os.listdir(direc) if f.endswith('.pkl')]
        
        # Move each file to the 'archive' directory
        for file in files:
            source_file = os.path.join(direc, file)
            destination_file = os.path.join(archive_path, file)
            shutil.move(source_file, destination_file)  # Move and replace

def confirm_and_execute(directories):
    response = 'y'
    if response.lower() != 'n':
        archive_pkl_files(directories)
        print("STARTING PROGRAM ... \n")
    else:
        print("Operation cancelled.")

# Directories list
directories = ["_1_tables", "_20_add_cash", "_21_add_ledger_sell", "_22_add_ledger_buy"]

# Call the function with confirmation
confirm_and_execute(directories)

####################################################################################
## Initial Investment
#
d_start_date = '2022-07-01'
total_inv = 100000 
start_date_reset = d_start_date

# #
## FNS
############################################################################ FETCH PRICES table
#exec(open(f"_0_b1_yf_fetched_table_updt_.py",encoding="utf-8").read()) 
#Load the DataFrame containing closing prices READ with date index
df_close = pd.read_pickle("_1_fetch/_0_fetched_stock_data_prices.pkl")
# Ensure that the index is of datetime type if it isn't already
if not pd.api.types.is_datetime64_any_dtype(df_close.index):
    df_close.index = pd.to_datetime(df_close.index)
# #############################################
# # existing Stocks add more modify later -CE 49 Aprl
# print('\n->', len(l_stocks_updt),f'Stocks being fetched from {d_start_date} till today') 
# # Define your list of stocks and start date
# stocks = l_stocks_updt 
# start_date = d_start_date  
# end_date = datetime.now().strftime("%Y-%m-%d")  # Today's date, you can change it
# ############### get table 
# df_close = check_and_process_data() ######################### this is an external function 




###########################################################################

### FNS 
#exec(open(f"_0_b2_fns_PORTFOLIO_updt.py",encoding="utf-8").read()) 

exec(open(f"_0_b2_fns_PORTFOLIO_updt.py",encoding="utf-8").read()) 


exec(open(f"_0_CashExcess_PORTFOLIO.py",encoding="utf-8").read()) 
## DEFENSIVE
exec(open(f"_0_D_PORTFOLIO_hist_.py",encoding="utf-8").read()) 
## Growght
exec(open(f"_0_G_PORTFOLIO_hist_.py",encoding="utf-8").read()) 

############################################################################
# # ############################################################################
# # ############################################################################
# # # HIST -> DATA
# # ############################################################################
# # ############################################################################

def concat_pkl_to_df(hist_df, directory=""):
    """

    """
    # Ensure the directory path ends with a slash
    directory = directory.rstrip('/') + '/'

    # Find all .pkl files in the specified directory
    pkl_files = glob.glob(f"{directory}*.pkl")

    # Read each .pkl file and concatenate it to hist_df
    for file_path in pkl_files:
        # Read the .pkl file
        df_entry = pd.read_pickle(file_path)

        # Concatenate the read DataFrame to hist_df
        hist_df = pd.concat([hist_df, df_entry], ignore_index=True)
        #hist_df = hist_df.append(df_entry, ignore_index=True)
    return hist_df

# CONCAT ALL HIST TO BE PROCESSED 

hist_df_0 = pd.concat([hist_df_d,hist_df_g], ignore_index=True)
df_add = concat_pkl_to_df(hist_df_0, directory="_2_tables_add/")
df_add = df_add.sort_values(by='DateTrans').copy().reset_index(drop=True)# SORT by dates

# # ############################################################################
# # ############################################################################
def get_unique_stocks(portfolio_labels_g,portfolio_labels_d,stock_list_ce,df_add):
    
    stocks_add_unique = set(df_add['Stock'])
    unique_exchange_stocks = set(x for sublist in df_add['exchange_stocks'] for x in sublist)
    # Combine both sets to get all unique stocks
    all_unique_stocks = stocks_add_unique.union(unique_exchange_stocks)
    # Convert the set back to a list if needed
    all_unique_stocks_list_df_add = list(all_unique_stocks)
    
    ##########
    
    # join all init 
    stock_list_all = portfolio_labels_g + portfolio_labels_d + stock_list_ce +all_unique_stocks_list_df_add 
    
    unique_stocks = list(set(stock_list_all))
    # GET rid of cash 
    l_stocks_updt = [stock for stock in unique_stocks if stock not in ['CASH', 'Cash']]

    return l_stocks_updt


####### get all unique stocks in portfolio

l_stocks_updt = get_unique_stocks(portfolio_labels_g,portfolio_labels_d,stock_list_ce,df_add)
print(len(l_stocks_updt))

# fetch prices if neccesary here 
df_close = master_fetch_check(l_stocks_updt,d_start_date)
print(df_close)
input('')
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
import pandas as pd
import ast
from datetime import datetime

# Assuming your DataFrames 'df_add' and 'df' are already defined and loaded

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

