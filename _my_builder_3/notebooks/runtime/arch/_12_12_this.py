

from _fns import sum_units_sold_by_stock_bought,sum_units_sold_by_stock_sold,sum_buy_sell_ordered,calculate_and_add_dividends
from _fns import fetch_stock_price_on_date_close



import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import glob
import os


#PROG VAR NAMES

name_1_a_Cash_Excess_calc = '_1_a_CASH_Excess_calculation'





# Set display options
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)        # Use maximum width of the console
pd.set_option('display.max_colwidth', 20)   # Set maximum column width (can adjust as needed)
pd.set_option('display.expand_frame_repr', True)  # Expand the DataFrame representation to stretch across multiple lines


# Get the current date and time
#


now = datetime.now();formatted_date_time = now.strftime("%Y_%m_%d_h%Hm%M");formatted_date_time

def merge_pickles(folder_path):
    data_frames = []
    for file in os.listdir(folder_path):
        if file.endswith('.pkl'):
            file_path = os.path.join(folder_path, file)
            df = pd.read_pickle(file_path)
            # Using list concatenation instead of append
            data_frames += [df]
    merged_df = pd.concat(data_frames, ignore_index=True)
    return merged_df


df_sell = merge_pickles('_21_add_ledger_sell')
df_buy = merge_pickles('_22_add_ledger_buy')
df_master_unit_updt = pd.read_pickle(f'_1_tables/_df_0_init_UNITS.pkl').sort_values(by='Stock')
##########################################################
stock_names = df_master_unit_updt['Stock']#[:-2].tolist()
df_all_sell = sum_units_sold_by_stock_sold(df_sell, stock_names)
df_all_buy =  sum_units_sold_by_stock_bought(df_buy, stock_names)
df_sum = sum_buy_sell_ordered(df_all_buy, df_all_sell)
#
df_all = pd.merge(df_master_unit_updt, df_sum, on='Stock', how='inner')
#
df_all['hold_units_CHECK'] = df_all['hold_units_at_init_day_1'] + df_all['Total Units Bought'] + df_all['Total Units Sold']
# # ############################################################################
# # ############################################################################

# If df_updt was previously created by slicing, ensure it's a standalone DataFrame
df_updt = df_all.copy()
## Add a new column for the vector string to df_updt for tracking the transaction fees added
df_updt['Transaction Fee Details'] = ''
# Iterate through the 'Stock' column in df_updt to update the fees and create the vector string
for stock in df_updt['Stock']:
    # Retrieve the initial transaction fee from df_updt for the current stock
    initial_fee = df_updt.loc[df_updt['Stock'] == stock, 'Transaction Fee (AUD)'].iloc[0]
    
    # Initialize the fee details with the initial transaction fee as a string
    fee_details = [str(initial_fee)]
    
    # Get the fees from df_sell and append them as strings to the fee_details list
    sell_fees = df_sell[df_sell['Stock'] == stock]['trans_fee']
    fee_details += sell_fees.astype(str).tolist()
    
    # Get the fees from df_buy and append them as strings to the fee_details list
    buy_fees = df_buy[df_buy['Stock'] == stock]['trans_fee']
    fee_details += buy_fees.astype(str).tolist()
    
    # Create the vector string of all transaction fees that will be summed
    vector_string = ' + '.join(fee_details)
    
    # Calculate the total transaction fee
    total_fee = initial_fee + sell_fees.sum() + buy_fees.sum()
    
    # Update the 'Transaction Fee (AUD)' column with the new total
    df_updt.loc[df_updt['Stock'] == stock, 'Transaction Fee (AUD)'] = total_fee
    
    # Update the 'Transaction Fee Details' column with the vector string
    df_updt.loc[df_updt['Stock'] == stock, 'Transaction Fee Details'] = vector_string

# ############################################################################ ::: SELL
# Select the desired columns to keep in a new DataFrame
selected_columns = [
    'Stock',   'StartDate', 'Transaction Fee (AUD)',
    'hold_units_at_init_day_1', 'hold_units_at_init', 'hold_units_CHECK'
]

# Create the new DataFrame with only the selected columns ALL
df_show = df_all[selected_columns]

# #
columns_to_keep_s = ['Stock', 'DateTrans']

# Columns you want to rename, specified as {'old_name': 'new_name'}
columns_to_rename_s = {
    'units_sold': 'units_updts',
    #'hold_units_at_init': 'NewHoldUnitsAtInit',
    #'hold_units_CHECK': 'NewHoldUnitsCheck'
}

# First, select all the columns (both to keep and to rename)
all_columns_s = columns_to_keep_s + list(columns_to_rename_s.keys())

df_sell_4_cash = df_sell[all_columns_s]

# Then, rename the specified columns
df_sell_4_cash = df_sell_4_cash.rename(columns=columns_to_rename_s)
df_sell_4_cash
#
############################################################################## ::: INIT
columns_to_keep = ['Stock', 'StartDate']

# Columns you want to rename, specified as {'old_name': 'new_name'}
columns_to_rename = {
    'hold_units_at_init_day_1': 'units_hold',
    #'hold_units_at_init': 'NewHoldUnitsAtInit',
    #'hold_units_CHECK': 'NewHoldUnitsCheck'
}

# First, select all the columns (both to keep and to rename)
all_columns = columns_to_keep + list(columns_to_rename.keys())

df_init_4_cash = df_updt[all_columns]

# Then, rename the specified columns
df_init_4_cash = df_init_4_cash.rename(columns=columns_to_rename)
df_init_4_cash    
   
############################################################################### ::: BUY
columns_to_keep_b = ['Stock', 'DateTrans']

# # Columns you want to rename, specified as {'old_name': 'new_name'}
columns_to_rename_b = {
    'units_acquired': 'units_updts',
    #'hold_units_at_init': 'NewHoldUnitsAtInit',
    #'hold_units_CHECK': 'NewHoldUnitsCheck'
}

# # First, select all the columns (both to keep and to rename)
all_columns_b = columns_to_keep_b + list(columns_to_rename_b.keys())

df_buy_4_cash = df_buy[all_columns_b]

# # Then, rename the specified columns
df_buy_4_cash = df_buy_4_cash.rename(columns=columns_to_rename_b)
df_buy_4_cash
# #
############################################
############################################

df = pd.concat([df_init_4_cash, df_sell_4_cash, df_buy_4_cash], ignore_index=True) 
df = df.sort_values(by=['Stock', 'StartDate', 'DateTrans']) # SORT

############################## GET df_div  ################################## :::  EXEC !

exec(open(f"{name_1_a_Cash_Excess_calc}.py",encoding="utf-8").read()) #paths

############################################
############################################ ADD ONS


# Assuming df_div is your DataFrame

# Convert 'EndDate' column to datetime if it's not already
df_div['EndDate'] = pd.to_datetime(df_div['EndDate'])
############################################ ADD ONS
############################################ ADD ONS
############################################ export df_div
#df_div.to_pickle(f'_1_tables/_df_div_11_breakdown_LEDGER.pkl')


############################################ ADD ONS
############################################ ADD ONS

# Group by 'Stock' and find the row with the maximum 'EndDate' for each group
latest_dates = df_div.groupby('Stock')['EndDate'].transform('max')

# Filter the DataFrame based on the latest dates
df_div_updt = df_div[df_div['EndDate'] == latest_dates].sort_values(by='Stock')

# Now filtered_df contains only the rows with the latest date for each stock

len(df_div_updt)# = df_div_updt[['Stock', 'units_hold']]

len(df_master_unit_updt) #= df[['Stock', 'hold_units_at_init']]

m_df = pd.merge(df_master_unit_updt[['Stock', 'hold_units_at_init']], df_div_updt[['Stock', 'units_hold','EndDate']], on='Stock', how='inner')
m_df.head()

# if equal_units then you will see ones (buy_sell tables = units uptd )

m_df['equal_units'] = (m_df['hold_units_at_init'] == m_df['units_hold']).astype(int)
#print(m_df.head())


############## if abve checks in then 
print('\nUNITS, CASH BALANCE, & Dividends with TACT custom looks good - NO WARNINGS !\n ')


# Get the set of stocks from each DataFrame
stocks_in_df_div_updt = set(df_div_updt['Stock'])
stocks_in_df_other = set(df['Stock'])

# Find the missing stock
missing_stock = stocks_in_df_div_updt.symmetric_difference(stocks_in_df_other)

#print("Missing stocks in ledger:", missing_stock)


############################################
################################################################ FNS
from datetime import datetime

def adjust_to_thursday(cutoff_date):
    """
    Adjust the date to ensure it's suitable for analysis, prioritizing Thursday,
    or Friday if Thursday isn't an option.
    
    :param cutoff_date: The original cutoff date.
    :return: Adjusted date.
    """
    # Adjust based on the specified date's weekday
    if cutoff_date.weekday() == 6:  # Sunday
        return cutoff_date - timedelta(days=3)  # Previous Thursday
    elif cutoff_date.weekday() == 5:  # Saturday
        return cutoff_date - timedelta(days=2)  # Previous Thursday
    elif cutoff_date.weekday() in [0, 1, 2, 3]:  # Monday to Thursday
        return cutoff_date + timedelta(days=(3 - cutoff_date.weekday()))
    
    return cutoff_date
    
###################

def filter_df_by_months(df, months_ago, date_column):
    """
    Filter a dataframe to exclude the last N months based on a date column.
    Adds columns with the current run date and the start date from which the algorithm counts back.
    
    :param df: DataFrame to filter.
    :param months_ago: Number of months ago to start excluding data from the DataFrame.
    :param date_column: Name of the column containing date information.
    :return: Filtered DataFrame.
    """
    # Ensure the date column is in datetime format
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Calculate the cutoff date to exclude data after this point
    today = datetime.today()
    cutoff_date = today - pd.DateOffset(months=months_ago)

    # Filter the DataFrame accordingly
    if months_ago == 0:
        filtered_df = df.copy()
    else:
        filtered_df = df[df[date_column] < cutoff_date].copy()  # Explicit copy to avoid SettingWithCopyWarning

    # Add new columns
    filtered_df['run_date'] = today.strftime('%Y-%m-%d')  # The date when the function is run
    filtered_df['count_back_from_date'] = (today - pd.DateOffset(months=months_ago)).strftime('%Y-%m-%d')  # The start date from which the algorithm counts back

    return filtered_df

###################
# Define the function to compare and create 'AnalysisEndDate'
def compare_and_set_analysis_end_date(df):
    # Ensure both columns are in datetime format
    df['EndDate'] = pd.to_datetime(df['EndDate'])
    df['count_back_from_date'] = pd.to_datetime(df['count_back_from_date'])
    
    # Adjust the condition as per the new requirement
    df['AnalysisEndDate'] = df.apply(lambda row: row['count_back_from_date'] if row['count_back_from_date'] < row['EndDate'] else row['EndDate'], axis=1)
    return df

###############################


################################################################

_df_0m = filter_df_by_months(df_div,0, 'StartDate')
_df_3m = filter_df_by_months(df_div,3, 'StartDate')
_df_6m = filter_df_by_months(df_div,6, 'StartDate')
_df_12m = filter_df_by_months(df_div,12, 'StartDate') # CHANGE to 12 months

# List of DataFrames for iteration
dfs = [_df_0m, _df_3m, _df_6m, _df_12m]

# Apply the function to each DataFrame
dfs = [compare_and_set_analysis_end_date(df) for df in dfs]

# Now, dfs contains the modified DataFrames with the correct 'AnalysisE
################################################################
################################################################ GET DIVIDENDS
# Initialize a cache for dividends to minimize API calls
dividend_cache = {}

# # Apply the function to each DataFrame
#_df_0m = calculate_and_add_dividends(_df_0m)
# _df_3m = calculate_and_add_dividends(_df_3m)
# _df_6m = calculate_and_add_dividends(_df_6m)
# _df_12m = calculate_and_add_dividends(_df_12m)

# 

# #calculate unit range hist with dividends
# df_hist_unit_divs = _df_0m

# ###############################################################

# # ADD DIV value  SUm
# _df_0m_info = _df_0m.groupby('Stock')['Dividends'].sum().reset_index().rename(columns={'Dividends': 'dividend_total'})
# _df_0m = _df_0m.merge(_df_0m_info, on='Stock').copy()

# # Sort by 'Stock' and 'AnalysisEndDate' in descending order
# _df_0m = _df_0m.sort_values(by=['Stock', 'AnalysisEndDate'], ascending=[True, False])

# # Drop duplicates based on 'Stock', keeping the first (most recent 'AnalysisEndDate')
# _df_0m = _df_0m.drop_duplicates(subset='Stock', keep='first')
# _df_0m['m_period']  = '0m'

# ################################################################
# ################################################################

# # ADD DIV value  SUm
# _df_3m_info = _df_3m.groupby('Stock')['Dividends'].sum().reset_index().rename(columns={'Dividends': 'dividend_total'})
# _df_3m = _df_3m.merge(_df_3m_info, on='Stock').copy()

# # Sort by 'Stock' and 'AnalysisEndDate' in descending order
# _df_3m = _df_3m.sort_values(by=['Stock', 'AnalysisEndDate'], ascending=[True, False])

# # Drop duplicates based on 'Stock', keeping the first (most recent 'AnalysisEndDate')
# _df_3m = _df_3m.drop_duplicates(subset='Stock', keep='first')
# _df_3m['m_period']  = '3m'
# ################################################################
# ################################################################

# # ADD DIV value  SUm
# _df_6m_info = _df_6m.groupby('Stock')['Dividends'].sum().reset_index().rename(columns={'Dividends': 'dividend_total'})
# _df_6m = _df_6m.merge(_df_6m_info, on='Stock').copy()

# # Sort by 'Stock' and 'AnalysisEndDate' in descending order
# _df_6m = _df_6m.sort_values(by=['Stock', 'AnalysisEndDate'], ascending=[True, False])

# # Drop duplicates based on 'Stock', keeping the first (most recent 'AnalysisEndDate')
# _df_6m = _df_6m.drop_duplicates(subset='Stock', keep='first')
# _df_6m['m_period'] = '6m'
# ################################################################
# ################################################################

# # ADD DIV value  SUm
# _df_12m_info = _df_12m.groupby('Stock')['Dividends'].sum().reset_index().rename(columns={'Dividends': 'dividend_total'})
# _df_12m = _df_12m.merge(_df_12m_info, on='Stock').copy()

# # Sort by 'Stock' and 'AnalysisEndDate' in descending order
# _df_12m = _df_12m.sort_values(by=['Stock', 'AnalysisEndDate'], ascending=[True, False])

# # Drop duplicates based on 'Stock', keeping the first (most recent 'AnalysisEndDate')
# _df_12m = _df_12m.drop_duplicates(subset='Stock', keep='first')
# _df_12m['m_period'] = '12m'

# ################################################################

# div_total_0 =_df_0m['dividend_total'].sum()
# div_total_3 =_df_3m['dividend_total'].sum()
# div_total_6 =_df_6m['dividend_total'].sum()
# div_total_12 =_df_12m['dividend_total'].sum()

# #print('\n\n ATTN ::: div_total 0,3,6,12 months resp:::\n',div_total_0,div_total_3,div_total_6,div_total_12,'\n\n',)

# ################################################################
# ################################################################
# # BUILD MASTER TABLE
# ################################################################
# ################################################################

# def concat_dfs(dfs, columns_to_keep=[]):
   
#     # Check if specific columns are provided for the final dataframe
#     if columns_to_keep:
#         # Filter each dataframe to keep only the specified columns (if they exist in that dataframe)
#         filtered_dfs = [df[columns_to_keep] for df in dfs if set(columns_to_keep).issubset(df.columns)]
#     else:
#         # If no columns are specified, use all dataframes as they are
#         filtered_dfs = dfs
    
#     # Concatenate all the filtered dataframes
#     final_df = pd.concat(filtered_dfs, ignore_index=True)
    
#     return final_df

# # Example usage:

# dfs = [_df_0m,_df_3m ,_df_6m,_df_12m]
# columns_to_keep = ['Stock','units_hold','m_period', 'dividend_total','AnalysisEndDate']
# df_master = concat_dfs(dfs, columns_to_keep)

# ################################################################
# #print(len(_df_0m),_df_0m.tail(21).sort_values(by='Stock'))

# ###################### WRITE 
# ######################
# ###################### VAR NAMES

# nme_df_hist_unit_divs = '_df_hist_12_up_to_date_DIV-UNITS' 
# nme_df_master = '_df_periods_123_monthly_df_HIST_'



# df_hist_unit_divs.to_pickle(f'_1_tables/{nme_df_hist_unit_divs}.pkl')
# df_master.to_pickle(f'_1_tables/{nme_df_master}.pkl')



# #print('12,123 EXPORTED \n')

# #.to_pickle(f'_1_tables/{}.pkl')








