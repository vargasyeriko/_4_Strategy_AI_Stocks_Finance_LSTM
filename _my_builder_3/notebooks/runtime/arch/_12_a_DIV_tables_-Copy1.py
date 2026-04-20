

from _fns import sum_units_sold_by_stock_bought,sum_units_sold_by_stock_sold,sum_buy_sell_ordered
from _fns import filter_df_by_months_and_analysis_dates_and_DIVS 
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

df_close = pd.read_pickle("_1_fetch/_0_fetched_stock_data_prices.pkl")
# Ensure that the index is of datetime type if it isn't already
if not pd.api.types.is_datetime64_any_dtype(df_close.index):
    df_close.index = pd.to_datetime(df_close.index)



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

# ############################################
# ############################################ ADD ONS -> this next function will generate new months by itself 
import pandas as pd

def create_master_df(df, start_date_str):
    start_date = pd.to_datetime(start_date_str)
    today = pd.Timestamp('today')
    
    # Calculate the number of months from the start date to now
    total_months = (today.year - start_date.year) * 12 + today.month - start_date.month
    
    # List to hold each DataFrame slice
    df_list = []
    
    # Generate DataFrames from now going back to the start date
    for months_back in range(total_months + 1):
        temp_df = filter_df_by_months_and_analysis_dates_and_DIVS(df, months_back, 'StartDate') #### imp
        temp_df = temp_df.copy()  # Make a copy to safely modify the DataFrame
        temp_df.loc[:, 'period'] = months_back  # Use .loc to set the 'period' column
        df_list.append(temp_df)
        
        # Check if we have reached or exceeded the start date limit
        if (today - pd.DateOffset(months=months_back)).date() < start_date.date():
            break
    
    # Concatenate all DataFrames into a master DataFrame
    df_master = pd.concat(df_list, ignore_index=True)
    return df_master

print('another d_start_date specified in here \n')
d_start_date = '2022-07-01'
df_master = create_master_df(df_div, d_start_date)

############################################################## DIVIDENDS

# BEFORE RETURNS copy master table with no deletions 

#print(div_pivot_table.head())

# Grouping by 'Stock' and 'period', then calculating the sum of 'Dividends'
dividends_sum = df_master.groupby(['Stock', 'period'])['Dividends'].sum().reset_index()
# Renaming the summed column
dividends_sum.rename(columns={'Dividends': 'total_divs'}, inplace=True)
# Merging the summed dividends back to the original dataframe
df_master = pd.merge(df_master, dividends_sum, on=['Stock', 'period'], how='left')

#input('')
################################ filtered DF  : df_add_divs : Stock, period, total_divs
df_add_divs= df_master.copy()
# # Dropping duplicates, keeping the last entry (most recent 'AnalysisEndDate') per 'Period' and 'Stock'
df_add_divs.sort_values(by=['period', 'AnalysisEndDate'], inplace=True)
df_add_divs = df_add_divs.drop_duplicates(subset=['period', 'Stock'], keep='last')
df_add_divs = df_add_divs[['Stock', 'period','total_divs']].copy()

#input('')

############################################################# filtered DF RETURNS ,
#no 0 units start, keep upddated 
#df_master work ::: FIRST DELETE ALL the rows where units =0 and d_start_date = Startdate
mask = (df_master['units_hold'] == 0.0000) & (df_master['StartDate'] == d_start_date).copy()
deleted_count = mask.sum().copy()  # prints how many rows it will delete
df_ret = df_master[~mask].copy()  # removes rows where the mask is True

############ now keep only the rows where Stock has the latest AnalysisEndDate
df_ret.sort_values(by=['period', 'AnalysisEndDate'], inplace=True)
# Dropping duplicates, keeping the last entry (most recent 'AnalysisEndDate') per 'Period' and 'Stock'
df_ret = df_ret.drop_duplicates(subset=['period', 'Stock'], keep='last').copy()

##################### fetch prices by period 
df_ret['price_end_date'] = df_ret.apply(
    lambda row: fetch_stock_price_on_date_close(row['Stock'], row['AnalysisEndDate'], df_close), axis=1)

#print(df_master[['Stock', 'AnalysisEndDate', 'price_end_date']])


##################### ##################### #####################  Merge df_add_divs & df_ret

# Initialize an empty DataFrame to store the combined results
df_report = pd.DataFrame()
# Iterate through each unique period available in df_add_divs
for period in df_add_divs['period'].unique():
    # Filter df_master and df_add_divs for the current period
    df_master_period = df_ret[df_ret['period'] == period].copy()
    df_add_divs_period = df_add_divs[df_add_divs['period'] == period]
    
    # Merge the DataFrames
    df_combined = df_add_divs_period.merge(df_master_period, on='Stock', how='outer', suffixes=('', '_master'))
    
    # Set 'AnalysisEndDate' from df_master_period if available
    if not df_master_period.empty:
        common_analysis_end_date = df_master_period['AnalysisEndDate'].iloc[0]
    else:
        common_analysis_end_date = 'No Date'  # Define a default if df_master_period is empty

    # Fill missing values in 'AnalysisEndDate' and other columns
    df_combined['AnalysisEndDate'].fillna(common_analysis_end_date, inplace=True)
    df_combined['total_divs'].fillna(0, inplace=True)

    # Fill other necessary defaults
    for column in df_combined.columns:
        if 'master' in column:  # Columns from df_master_period might have suffix '_master'
            clean_column = column.replace('_master', '')
            df_combined[clean_column].fillna(df_combined[column], inplace=True)
            df_combined.drop(column, axis=1, inplace=True)  # Drop master columns after filling
        elif df_combined[column].dtype == 'float64':
            df_combined[column].fillna(0, inplace=True)
        elif df_combined[column].dtype == 'object' and column.endswith('Date') and column != 'AnalysisEndDate':
            df_combined[column].fillna('No Date', inplace=True)  # or a specific default date if needed

    # Append the combined DataFrame of the current period to the final DataFrame
    df_report = pd.concat([df_report, df_combined], ignore_index=True)

# Reset index in the final DataFrame to ensure unique indexing
df_report.reset_index(drop=True, inplace=True)

df_report = df_report[['Stock', 'units_hold', 'AnalysisEndDate', 'period',
                      'price_end_date','total_divs']].copy()


## FINALLY GET holding value per Stock
df_report['stock_value_hold'] = df_report['units_hold'] * df_report['price_end_date']

# SORT
df_report = df_report.sort_values(by=['period','Stock'])

# until here that lenght :: print(len(df_report)) / n of periods  should be equal to all stock no. in hist

######################## df_report has monthly dividends and returns hoding value. there are 0 in prices that were not in df_ret

######################################### ADD CASH :::
name_cash_init_modif  = '_df_cash_init_1_empty_CASH'
df_cash = pd.read_pickle(f'_20_add_cash/{name_cash_init_modif}.pkl')

# New column initialization
df_report['period_cash'] = 0.0

# Iterate over df_report and update 'cash' based on conditions
for index, row in df_report.iterrows():
    # Summing amounts where DateTrans is less than AnalysisEndDate
    sum_amount = df_cash[(df_cash['DateTrans'] < row['AnalysisEndDate'])]['amount'].sum()
    df_report.at[index, 'period_cash'] = sum_amount

######################################### make a few last adjustments :::: 

##### ***** 1 # GET total DIVS by period (the stock dividend amount is in total_divs), and 

# Group by 'period' and sum 'total_divs', then merge this back to the original df_report
total_divs_by_period = df_report.groupby('period')['total_divs'].sum().reset_index()
total_divs_by_period.rename(columns={'total_divs': 'period_divs'}, inplace=True)

# Merge this aggregated data back to the original DataFrame
df_report = pd.merge(df_report, total_divs_by_period, on='period', how='left')

##### ***** 1.2 get period cash excess = (period_cash	 + period_divs)

df_report['period_total_cash'] = df_report['period_cash'] + df_report['period_divs']


##### ***** 2 # GET total stock  HOLDING value , and period holding value 

# Group by 'period' and sum 'stock_value_hold', then merge this back to the original df_report
total_stock_value_by_period = df_report.groupby('period')['stock_value_hold'].sum().reset_index()
total_stock_value_by_period.rename(columns={'stock_value_hold': 'period_stocks_value'}, inplace=True)

# Merge this aggregated data back to the original DataFrame
df_report = pd.merge(df_report, total_stock_value_by_period, on='period', how='left')

##### ***** 3 # GET TOTAL portfolio holding Value 

df_report['period_total_holds'] = df_report['period_total_cash'] + df_report['period_stocks_value']

########## 4 final adjustments and pivot tables :::
# round 
columns_to_round = [
    'units_hold', 'price_end_date', 'total_divs',
    'stock_value_hold', 'period_divs','period_total_cash', 
    'period_stocks_value','period_total_holds']
# Rounding the specified columns
# Rounding the specified columns
for column in columns_to_round:
    if column in df_report.columns:  # Check if column exists to prevent errors
        # Apply rounding directly
        df_report[column] = df_report[column].apply(lambda x: round(x, 2) if pd.notnull(x) else x)



###### 5 pivot tables 


# # Aggregate 'Dividends' by 'Stock' and 'period 
# aggregated_data = df_master.groupby(['Stock', 'period'])['Dividends'].sum().reset_index()
# # Pivot the table to see 'Dividends' for each 'period ' by 'Stock'
# div_pivot_table_master = aggregated_data.pivot(index='Stock', columns='period', values='Dividends').fillna(0)



# # Assuming df_div is your DataFrame

# # Convert 'EndDate' column to datetime if it's not already
# df_div['EndDate'] = pd.to_datetime(df_div['EndDate'])
# ############################################ ADD ONS
# ############################################ ADD ONS
# ############################################ export df_div
# #df_div.to_pickle(f'_1_tables/_df_div_11_breakdown_LEDGER.pkl')
# ########################################### ADD ONS
# ############################################ ADD ONS
# # Group by 'Stock' and find the row with the maximum 'EndDate' for each group
# latest_dates = df_div.groupby('Stock')['EndDate'].transform('max')
# # Filter the DataFrame based on the latest dates
# df_div_updt = df_div[df_div['EndDate'] == latest_dates].sort_values(by='Stock')
# # Now filtered_df contains only the rows with the latest date for each stock
# len(df_div_updt)# = df_div_updt[['Stock', 'units_hold']]
# len(df_master_unit_updt) #= df[['Stock', 'hold_units_at_init']]
# m_df = pd.merge(df_master_unit_updt[['Stock', 'hold_units_at_init']], df_div_updt[['Stock', 'units_hold','EndDate']], on='Stock', how='inner')
# m_df.head()
# # if equal_units then you will see ones (buy_sell tables = units uptd )
# m_df['equal_units'] = (m_df['hold_units_at_init'] == m_df['units_hold']).astype(int)
# #print(m_df.head())
# ############## if abve checks in then 
# print('\nUNITS, CASH BALANCE, & Dividends with TACT custom looks good - NO WARNINGS !\n ')
# # Get the set of stocks from each DataFrame
# stocks_in_df_div_updt = set(df_div_updt['Stock'])
# stocks_in_df_other = set(df['Stock'])
# # Find the missing stock
# missing_stock = stocks_in_df_div_updt.symmetric_difference(stocks_in_df_other)
# #print("Missing stocks in ledger:", missing_stock)


################################################################

# _df_0m = filter_df_by_months_and_analysis_dates_and_DIVS(df_div,0, 'StartDate')

# _df_1m = filter_df_by_months_and_analysis_dates_and_DIVS(df_div,1, 'StartDate')
# _df_2m = filter_df_by_months_and_analysis_dates_and_DIVS(df_div,2, 'StartDate')

#_df_3m = filter_df_by_months(df_div,3, 'StartDate')
#_df_6m = filter_df_by_months(df_div,6, 'StartDate')
#_df_12m = filter_df_by_months(df_div,12, 'StartDate') # CHANGE to 12 months

# # List of DataFrames for iteration
# dfs = [_df_0m, _df_3m, _df_6m, _df_12m]

# # Apply the function to each DataFrame
# dfs = [compare_and_set_analysis_end_date(df) for df in dfs]

# # Now, dfs contains the modified DataFrames with the correct 'AnalysisE
# ################################################################
# ################################################################ GET DIVIDENDS
# # Initialize a cache for dividends to minimize API calls
# dividend_cache = {}

# # # Apply the function to each DataFrame
# _df_0m = calculate_and_add_dividends(_df_0m)
# _df_3m = calculate_and_add_dividends(_df_3m)
# _df_6m = calculate_and_add_dividends(_df_6m)
# _df_12m = calculate_and_add_dividends(_df_12m)

# #print(_df_0m)
# # 

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








