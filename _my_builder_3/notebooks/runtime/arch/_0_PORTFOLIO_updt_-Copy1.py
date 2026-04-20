###############################################
############################################################################
# PACKAGES
############################################################################
import pandas as pd
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import glob
#

# Get the current date and time
#
now = datetime.now();formatted_date_time = now.strftime("%Y_%m_%d_h%Hm%M");formatted_date_time
#
## Initial Investment
#
d_start_date = '2022-07-01'
total_inv = 100000 
# #
## FNS
#
############################################################################
### FNS
exec(open(f"_0_b_fns_PORTFOLIO_updt.py",encoding="utf-8").read()) 
## DEFENSIVE
exec(open(f"_0_D_PORTFOLIO_hist_.py",encoding="utf-8").read()) 
## Growght
exec(open(f"_0_G_PORTFOLIO_hist_.py",encoding="utf-8").read()) 

############################################################################
#
# # read both tables 
# df_init = pd.read_pickle('')
#df = 


# # ############################################################################
# # ############################################################################
# # # HIST -> DATA
# # ############################################################################
# # ############################################################################

# import pandas as pd
hist_df_0 = pd.concat([hist_df_d,hist_df_g], ignore_index=True);hist_df_0

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

    return hist_df

df_add = concat_pkl_to_df(hist_df_0, directory="_2_tables_add/")
df_add = df_add.sort_values(by='DateTrans').copy().reset_index(drop=True)# SORT by dates

# ############################################################################
# ############################################################################

#print(f'\n\n all_hist_df :: \n\n {len(df_add)}')

# df_add.to_pickle(f'_1_tables/_1_up_to_date_historic.pkl')
# print('\n df_now broght in sells  df_now  :\n')

# ############################################################################
# ############################################################################
df_g = df_g.iloc[:-2]
df_d = df_d.iloc[:-2]
df = pd.concat([df_d,df_g], ignore_index=True) # concat
df
# ############################################################################
# ############################################################################
# ############################################################################
# ############################################################################
# ############################################################################
# ############################################################################
# ############################################################################
# ############################################################################
# ############################################################################
###########################################################################
############################################################################
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
    df = df.append({'Stock': stock,  'Price Bought': 0, 'Latest Price': 0, 'Invested Amount (AUD)': 0, 'Transaction Fee (AUD)': 0,'Net Cash Value (AUD)': 0,
                   'StartDate': earliest_date_str, 'Percentage': 0, 'hold_units_at_init': 0,}, ignore_index=True)

# Ensure 'StartDate' column exists in 'df' and is properly formatted
if 'StartDate' not in df.columns:
    df['StartDate'] = pd.NaT  # Initialize 'StartDate' column if it doesn't exist

    
########################################### EXPORT 0 ::: df_0_upft_units.pkl :::: UNITS INIT
    
df.to_pickle(f'_1_tables/_df_0_init_UNITS.pkl')

########################################### EXPORT 1 ::: _df_cash_init_1_init_CASH.pkl # ::::: CASH INIT

cash_start_value = cash_start_value_d+cash_start_value_g

data = {
    'amount': cash_start_value,  # Scalar value
    'DateTrans': d_start_date,  # Scalar value
    'id_time_buy': f'Def_init_INV_{d_start_date}',  # Scalar value
    'trans_type': 'cash_init',  # Scalar value
    'costs': 0  # Scalar value
}
# You can create an index as a list with a single element if there is only one row of data
index = [0]  # Single row DataFrame
df_cash_init = pd.DataFrame(data, index=index).sort_values(by='DateTrans').reset_index(drop=True)


df_cash_init.to_pickle(f'_1_tables/_df_cash_init_1_init_CASH.pkl') #cashete

########################################### EXPORT 2 ...df_add_1_up_to_date_historic # ::::: CASH INIT


df_add.to_pickle(f'_1_tables/_df_add_2_up_to_date_historic.pkl')
print('\n df_add with ALL Exchange transaction collection written df_1  :\n')    


########################################### EXPORT 2 ...








# # Create a new row to append to df_cash_bal
# new_row = {
#     'amount': cash_start_value,  # Adding cash_start_value to amount
#     'DateTrans': d_start_date,  # Setting DateTrans to d_start_date
#     'id_time_buy': f'Def_init_INV_{d_start_date}',  # Setting id to 'Def_init_INV_{d_start_date}'
#     'trans_type': 'cash_init',  # Setting transaction type to 'cash_init'
#     'costs': 0  # Setting costs to 0
# }

# # Append the new row to df_cash_bal
# df_cash_bal = df_cash_bal.append(new_row, ignore_index=True)


# # Step 1: Flag rows where 'Stock' is either 'Cash' or 'trans_cost'
# df['is_target'] = df['Stock'].isin(['Cash', 'trans_cost'])

# # Step 2: Sort the DataFrame to move flagged rows to the bottom
# df = df.sort_values(by='is_target', ascending=True)

# # Step 3: Drop the temporary flag column
# df.drop('is_target', axis=1, inplace=True)

# #print('df has been updatede with all ne added stocks after start date ')
# portfolio_df_init =df
# df['hold_units_at_init_day_1']= portfolio_df_init['hold_units_at_init']

# ############################################################################
# ############################################################################
# #cash = 90
# #Convert the 'TransDate' column to datetime format if it's not already
# df_add['DateTrans'] = pd.to_datetime(df_add['DateTrans'])

# # Now that 'TransDate' is guaranteed to be in datetime format, format it to a string
# df_add['DateTrans'] = df_add['DateTrans'].dt.strftime('%Y-%m-%d')

# ############################################################################
# ############################################################################
# import pandas as pd
# import yfinance as yf
# from datetime import datetime

# def fetch_stock_price_on_date(stock_symbol, date):
#     """
#     Fetches the closing price of a stock on a specific date using yfinance.
#     Expands the search range to accommodate for weekends and holidays.
#     """
#     try:
#         start_date = (datetime.strptime(date, "%Y-%m-%d") - pd.Timedelta(days=2)).strftime("%Y-%m-%d")
#         end_date = (datetime.strptime(date, "%Y-%m-%d") + pd.Timedelta(days=2)).strftime("%Y-%m-%d")
#         stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

#         if not stock_data.empty:
#             if date in stock_data.index.strftime("%Y-%m-%d").tolist():
#                 return stock_data.loc[date]['Close']
#             else:
#                 return stock_data['Close'].iloc[0]
#     except Exception as e:
#         print(f"Error fetching data for {stock_symbol} on {date}: {e}")
#     return None

# def calculate_transaction(hold_units_at_init, stock, trans_date, trans_type, percentage):
#     """
#     Calculates a transaction based on the initial units held and the other transaction inputs.
#     Includes transaction fee calculation based on the transaction amount.
#     """
#     stock_price_at_trans = fetch_stock_price_on_date(stock, trans_date)

#     if stock_price_at_trans is None:
#         print(f"Could not fetch price for {stock} on the transaction date.")
#         return None

#     # Calculate transaction units based on percentage
#     trans_units = hold_units_at_init * (percentage / 100.0)
#     trans_amount = trans_units * stock_price_at_trans  # Calculate transaction amount based on current price

#     if trans_type == 's':
#         trans_units = -trans_units  # Negate units for sales

#     # Calculate transaction fee
#     trans_fee = trans_amount * 0.0009 if trans_amount > 7334 else 6.60

#     transaction = {
#         'Stock': stock,
#         'trans_type': trans_type,
#         'trans_date': trans_date,
#         'stock_price_at_trans': stock_price_at_trans,
#         'trans_units': trans_units,
#         'trans_amount': trans_amount,
#         'trans_fee': trans_fee,
#     }

#     df_transaction = pd.DataFrame([transaction])
#     df_transaction['net_cash'] = df_transaction['trans_amount'][0] - df_transaction['trans_fee'][0]
    
#     return df_transaction['trans_units'][0] , df_transaction['net_cash'][0], df_transaction['trans_fee'][0],df_transaction['trans_amount'][0]        

# ############################################################################
# ############################################################################
# import pandas as pd

# # Assuming df_add and df are your DataFrames and are already defined

# for index, row in df_add.iterrows():
#     stock_id = row['Stock']
#     trans_date = row['DateTrans']
#     trans_type = row['trans_type']
#     percentage = row['PercentSold']
#     ids_ = row['id_time']
    
#     # Find 'hold_units_at_init' in df where 'Stock' matches 'stock_id'
#     if stock_id in df['Stock'].values:
#         # Assuming 'Stock' is the column in df to match with 'stock_id'
#         # And assuming 'hold_units_at_init' is the column you're interested in from df
#         hold_units_at_init_row = df.loc[df['Stock'] == stock_id, 'hold_units_at_init']
#         hold_units_at_init = hold_units_at_init_row.iloc[0] if not hold_units_at_init_row.empty else None
#     else:
#         hold_units_at_init = None  # Default value if not found
    
#     # Assuming you have a function calculate_transaction defined somewhere
#     # Check if hold_units_at_init is found (not None) before calling
#     if hold_units_at_init is not None:
        
#         units_sold,add_to_cash, trans_fee_add,before_trans_fee = calculate_transaction(hold_units_at_init, stock_id, trans_date, trans_type, percentage)
#         # CALCULATE NEW UNITS BALANCE
#         unit_bal = hold_units_at_init + units_sold
        
#         df_add.loc[df_add['id_time'] == ids_, 'buy_amount'] = add_to_cash
#         df_add.loc[df_add['id_time'] == ids_, 'units_sold'] = units_sold # add a value to 
#         df_add.loc[df_add['id_time'] == ids_, 'trans_fee'] = trans_fee_add # add a value to 

#         df_add.loc[df_add['id_time'] == ids_, 'before_trans_fee'] = before_trans_fee # add a value to 

        
#         print(f'\nUnits HOLDS at Init: {hold_units_at_init}, \nUnits SOLD ::: ',units_sold, '\nUnits UPDATE at : ',unit_bal )
        
#         # IF UNIT BALANCE CHANGE go CHANGE it
#         if unit_bal != hold_units_at_init:
#             df.loc[df['Stock'] == stock_id, 'hold_units_at_init'] = unit_bal
#             print(f"The hold_units_at_init value for {stock_id} has been updated to: {unit_bal} UNITS",'>>> exchange to $$$ \t for buys ::', add_to_cash)
        
        
        
        
#     # Print the transaction details
#     print(f"\t\t\t\t---------> ---------> --------->---------> Stock ID >>> {stock_id}, \n\t\t\t\tDateTrans: {trans_date}, \n\t\t\t\tTransaction Type: {trans_type}")

# stocks_sell   = df_add['exchange_stocks'].tolist()

# percents_sell = df_add['sell_perc'].tolist()
# import ast

# # Assuming df_add['sell_perc'] contains strings that represent lists
# percents_sell = df_add['sell_perc'].tolist()

# # Convert the string representation of lists into actual lists
# percents_sell = [ast.literal_eval(item) if isinstance(item, str) else item for item in percents_sell]

# # Convert each item in each list to an integer
# percents_sell = [[int(item) for item in sublist] for sublist in percents_sell]


# amounts_split = df_add['buy_amount'].tolist()

# dates_sell    = df_add['DateTrans'].tolist()

# ids_sell      = df_add['id_time'].tolist()

# print('amounts split or not -> to buy',amounts_split)
# print(' \n\n# UPDATING PORTFOLIO -> allocations of buys :::\n\n ')
# # ############################################################################
# # ############################################################################

# # ############################################################################
# # ############################################################################
# import yfinance as yf
# import pandas as pd
# from datetime import datetime

# def fetch_stock_price_on_date(stock_symbol, date):
#     """
#     Fetches the closing price of a stock on a specific date using yfinance.
#     Expands the search range to accommodate for weekends and holidays.
#     """
#     try:
#         start_date = (datetime.strptime(date, "%Y-%m-%d") - pd.Timedelta(days=2)).strftime("%Y-%m-%d")
#         end_date = (datetime.strptime(date, "%Y-%m-%d") + pd.Timedelta(days=2)).strftime("%Y-%m-%d")
#         stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
        
#         if not stock_data.empty:
#             if date in stock_data.index.strftime("%Y-%m-%d").tolist():
#                 return stock_data.loc[date]['Close']
#             else:
#                 return stock_data['Close'].iloc[0]
#     except Exception as e:
#         print(f"Error fetching data for {stock_symbol} on {date}: {e}")
#         return None

# def buy_stocks(ids, stocks, percents, amounts, dates):
#     transactions = []
    
#     for id, stock_list, percent_list, amount, date in zip(ids, stocks, percents, amounts, dates):
#         for stock, percent in zip(stock_list, percent_list):
#             stock_price = fetch_stock_price_on_date(stock, date)
#             if stock_price is not None:
#                 money_allocated = amount * (percent / 100)
                
#                 trans_fee = money_allocated * 0.0009 if money_allocated > 7334 else 6.60
                
#                 money_allocated_trans_fee =  money_allocated -trans_fee
                
#                 # transactions COSTS
                
                
#                 units_bought = money_allocated_trans_fee / stock_price
                
#                 transactions.append({
#                     "Stock": stock,
#                     "Amount Bought":money_allocated_trans_fee,

#                     'keep_drop': 'd',
#                     'trans_type':'b',
#                     "DateTrans": date,
#                     "id_time": id,
#                     "id_time_buy": id + 'b_'+ stock,
#                     "Stock Price": stock_price,
#                     "units_acquired": units_bought,
#                     "trans_fee": trans_fee,
                    
#                     "Amount Bought_no_tf": money_allocated
#                 })
    
#     return pd.DataFrame(transactions)

# # Example usage
# ids = ids_sell
# stocks = stocks_sell
# percents = percents_sell
# amounts = amounts_split
# dates = dates_sell

# df_buy = buy_stocks(ids, stocks, percents, amounts, dates)

# df_buy


# # Creating df_cash with rows where Stock equals 'CASH'
# df_cash = df_buy[df_buy['Stock'] == 'CASH']

# # Creating df_no_cash with rows where Stock does not equal 'CASH'
# df_buy = df_buy[df_buy['Stock'] != 'CASH'].copy()
# df = df[df['Stock'] != 'CASH'].copy()
# ############################################################################
# ############################################################################
# import pandas as pd

# # Assuming df and df_buy are your DataFrames and are already defined

# for index, row in df_buy.iterrows():
#     stock_id = row['Stock']
#     trans_date = row['DateTrans']
#     trans_type = row['trans_type']
#     id_time_b = row['id_time_buy']  # Assuming this is your unique transaction identifier

#     # Find 'hold_units_at_init' in df where 'Stock' matches 'stock_id'
#     if stock_id in df['Stock'].values:
#         hold_units_at_init_row = df.loc[df['Stock'] == stock_id, 'hold_units_at_init']
#         hold_units_at_init = hold_units_at_init_row.iloc[0] if not hold_units_at_init_row.empty else None
#     else:
#         hold_units_at_init = None  # Default value if not found

#     # Check if hold_units_at_init is found (not None) before calling
#     if hold_units_at_init is not None:
#         # Calculate new units balance
#         units_bought = row['units_acquired']  # Directly use the row value for units acquired
#         unit_bal = hold_units_at_init + units_bought

#         print(f'\nUnits HOLDS at Init: {hold_units_at_init}, \nUnits BOUGHT ::: {units_bought}, \nUnits UPDATE at : {unit_bal}')

#         # If unit balance changes, go change it
#         if unit_bal != hold_units_at_init:
#             # Assuming you need to update the initial DataFrame 'df' with the new balance
#             df.loc[df['Stock'] == stock_id, 'hold_units_at_init'] = unit_bal
#             print(f"The hold_units_at_init value for {stock_id} has been updated to: {unit_bal}")

#     # Print the transaction details
#     print(f"\t\t\t\t---------> Stock ID: {stock_id}, \n\t\t\t\tDateTrans: {trans_date}, \n\t\t\t\tTransaction Type: {trans_type}")

# ############################################################################
# ############################################################################
# # CHECK
# print('\n\n')
# ############################################################################
# ############################################################################
# stock_names = df['Stock']#[:-2].tolist()
# df_all_sell = sum_units_sold_by_stock_sold(df_add, stock_names)
# df_all_buy =  sum_units_sold_by_stock_bought(df_buy, stock_names)
# df_sum = sum_buy_sell_ordered(df_all_buy, df_all_sell)
# df_all = pd.merge(df, df_sum, on='Stock', how='inner')
# df_all['hold_units_CHECK'] = df_all['hold_units_at_init_day_1'] + df_all['Total Units Bought'] + df_all['Total Units Sold']
# # ############################################################################
# # ############################################################################

# # Set display options
# pd.set_option('display.max_columns', None)  # Show all columns
# pd.set_option('display.width', None)        # Use maximum width of the console
# pd.set_option('display.max_colwidth', 20)   # Set maximum column width (can adjust as needed)
# pd.set_option('display.expand_frame_repr', True)  # Expand the DataFrame representation to stretch across multiple lines
# #pd.set_option('display.float_format', '{:.2f}'.format)  # Format floating points to show two decimal places

# # Assuming df_all is your DataFrame
# #print(df_all)

# # Assuming df_all is your DataFrame

# ############################################################################
# ############################################################################
# ## TABLE MODIFICATIONS

# # ############################################################################
# # ############################################################################


# # TO DADD ::: 'Price Bought', 'Latest Price' # SELL
# df_sell = df_add.copy()
# # BUY' df_buy

# # If df_updt was previously created by slicing, ensure it's a standalone DataFrame
# df_updt = df_all.copy()
# ## Add a new column for the vector string to df_updt for tracking the transaction fees added
# df_updt['Transaction Fee Details'] = ''
# # Iterate through the 'Stock' column in df_updt to update the fees and create the vector string
# for stock in df_updt['Stock']:
#     # Retrieve the initial transaction fee from df_updt for the current stock
#     initial_fee = df_updt.loc[df_updt['Stock'] == stock, 'Transaction Fee (AUD)'].iloc[0]
    
#     # Initialize the fee details with the initial transaction fee as a string
#     fee_details = [str(initial_fee)]
    
#     # Get the fees from df_sell and append them as strings to the fee_details list
#     sell_fees = df_sell[df_sell['Stock'] == stock]['trans_fee']
#     fee_details += sell_fees.astype(str).tolist()
    
#     # Get the fees from df_buy and append them as strings to the fee_details list
#     buy_fees = df_buy[df_buy['Stock'] == stock]['trans_fee']
#     fee_details += buy_fees.astype(str).tolist()
    
#     # Create the vector string of all transaction fees that will be summed
#     vector_string = ' + '.join(fee_details)
    
#     # Calculate the total transaction fee
#     total_fee = initial_fee + sell_fees.sum() + buy_fees.sum()
    
#     # Update the 'Transaction Fee (AUD)' column with the new total
#     df_updt.loc[df_updt['Stock'] == stock, 'Transaction Fee (AUD)'] = total_fee
    
#     # Update the 'Transaction Fee Details' column with the vector string
#     df_updt.loc[df_updt['Stock'] == stock, 'Transaction Fee Details'] = vector_string

# # Display the updated df_updt DataFrame
# pd.set_option('display.max_colwidth', None)
# trans_cost_all_but_cash_stock_buys = df_updt['Transaction Fee (AUD)'].sum()


# ############################################################################
# ############################################################################
# # Select the desired columns to keep in a new DataFrame
# selected_columns = [
#     'Stock',   'StartDate', 'Transaction Fee (AUD)',
#     'hold_units_at_init_day_1', 'hold_units_at_init', 'hold_units_CHECK'
# ]

# # Create the new DataFrame with only the selected columns ALL
# df_show = df_all[selected_columns]
# ############################################################################
# ############################################################################
# print(df_show)
# ############################################################################
# ############################################################################

# # TILL HERE the most updates tables for 
# ########################################
# print('\n\nRE-ARRANGING - TABLES','\n\n**********************************************************')
# ############################################################################################ ::: INIT
# # INIT =  df_updt : previous df_all (with sums) previous was df and virgin init portfolio_df
# # #
# columns_to_keep = ['Stock', 'StartDate']

# # Columns you want to rename, specified as {'old_name': 'new_name'}
# columns_to_rename = {
#     'hold_units_at_init_day_1': 'units_hold',
#     #'hold_units_at_init': 'NewHoldUnitsAtInit',
#     #'hold_units_CHECK': 'NewHoldUnitsCheck'
# }

# # First, select all the columns (both to keep and to rename)
# all_columns = columns_to_keep + list(columns_to_rename.keys())

# df_init_4_cash = df_updt[all_columns]

# # Then, rename the specified columns
# df_init_4_cash = df_init_4_cash.rename(columns=columns_to_rename)
# df_init_4_cash
# # Now, df_all_se
# ############################################################################################  ::: SELL
# # SELL = df_sell : previous was df_add
# #
# # #
# columns_to_keep_s = ['Stock', 'DateTrans']

# # Columns you want to rename, specified as {'old_name': 'new_name'}
# columns_to_rename_s = {
#     'units_sold': 'units_updts',
#     #'hold_units_at_init': 'NewHoldUnitsAtInit',
#     #'hold_units_CHECK': 'NewHoldUnitsCheck'
# }

# # First, select all the columns (both to keep and to rename)
# all_columns_s = columns_to_keep_s + list(columns_to_rename_s.keys())

# df_sell_4_cash = df_sell[all_columns_s]

# # Then, rename the specified columns
# df_sell_4_cash = df_sell_4_cash.rename(columns=columns_to_rename_s)
# df_sell_4_cash
# #
# ############################################################################################ ::: BUY
# # BUY = df_buy
# #
# # #
# columns_to_keep_b = ['Stock', 'DateTrans']

# # # Columns you want to rename, specified as {'old_name': 'new_name'}
# columns_to_rename_b = {
#     'units_acquired': 'units_updts',
#     #'hold_units_at_init': 'NewHoldUnitsAtInit',
#     #'hold_units_CHECK': 'NewHoldUnitsCheck'
# }

# # # First, select all the columns (both to keep and to rename)
# all_columns_b = columns_to_keep_b + list(columns_to_rename_b.keys())

# df_buy_4_cash = df_buy[all_columns_b]

# # # Then, rename the specified columns
# df_buy_4_cash = df_buy_4_cash.rename(columns=columns_to_rename_b)
# df_buy_4_cash
# # #
# ############################################################################################ ::: MERGE and SHOWCASE
# print('\n',df_init_4_cash.head(1),'\n\n',df_sell_4_cash.head(1),'\n\n',df_buy_4_cash.head(1))
# #
# #
# # SHOWCASE changes in df_show
# #
# df = pd.concat([df_init_4_cash, df_sell_4_cash, df_buy_4_cash], ignore_index=True) # concat
# df = df.sort_values(by=['Stock', 'StartDate', 'DateTrans']) # SORT
# print('\n\nCONCAT final :df \n\n',df,'\n\n**********************************************************')


# ############################################################################
# ############################################################################
# *********************************************************** ')
# ############################################################################
# ############################################################################

# ############################################################################
# ############################################################################

# ############################################################################
# ############################################################################




# ############################################################################
# ############################################################################

# ############################################################################
# ############################################################################

# ############################################################################
# ############################################################################

# ############################################################################
# ############################################################################


