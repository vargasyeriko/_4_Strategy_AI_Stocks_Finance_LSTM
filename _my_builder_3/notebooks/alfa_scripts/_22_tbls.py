import glob
import os
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
#
from _fns import sum_units_sold_by_stock_bought,sum_units_sold_by_stock_sold,sum_buy_sell_ordered
from _fns import filter_df_by_months_and_analysis_dates_and_DIVS 
from _fns import fetch_stock_price_on_date_close
from _0_b_fns_PORTFOLIO_updt import to_df_div
from _0_0_all_stocks_ import d_start_date,formatted_date_time
#
#PROG VAR NAMES
#
df_close = pd.read_pickle("_1_fetch/_0_fetched_stock_data_prices.pkl")
# Ensure that the index is of datetime type if it isn't already
if not pd.api.types.is_datetime64_any_dtype(df_close.index):
    df_close.index = pd.to_datetime(df_close.index)
#
# now = datetime.now();formatted_date_time = now.strftime("%Y_%m_%d_h%Hm%M");formatted_date_time
# Set display options
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)        # Use maximum width of the console
pd.set_option('display.max_colwidth', 20)   # Set maximum column width (can adjust as needed)
pd.set_option('display.expand_frame_repr', True)  # Expand the DataFrame representation to stretch across multiple lines
######


######
def get_df_ledger():
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
        'hold_units_at_init_day_1', 'hold_units_at_init', 'hold_units_CHECK']
    
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
        'hold_units_at_init_day_1': 'units_hold'}
    
    # First, select all the columns (both to keep and to rename)
    all_columns = columns_to_keep + list(columns_to_rename.keys())
    
    df_init_4_cash = df_updt[all_columns]
    #
    # Then, rename the specified columns
    df_init_4_cash = df_init_4_cash.rename(columns=columns_to_rename)
    ############################################################################### ::: BUY
    columns_to_keep_b = ['Stock', 'DateTrans']
    
    # # Columns you want to rename, specified as {'old_name': 'new_name'}
    columns_to_rename_b = {'units_acquired': 'units_updts'}
    
    # # First, select all the columns (both to keep and to rename)
    all_columns_b = columns_to_keep_b + list(columns_to_rename_b.keys())
    df_buy_4_cash = df_buy[all_columns_b]
    # # Then, rename the specified columns
    df_buy_4_cash = df_buy_4_cash.rename(columns=columns_to_rename_b)
    # #
    ############################################
    ############################################
    
    df = pd.concat([df_init_4_cash, df_sell_4_cash, df_buy_4_cash], ignore_index=True) 
    df = df.sort_values(by=['Stock', 'StartDate', 'DateTrans']) # SORT
    # br_cost= df_updt['Transaction Fee (AUD)'].sum() #BROCKAGE  COSTS
    # df_costs = df.copy()
    
    # df.to_pickle('_1_tables/_df_costs_1_2_complete_LEDGER.pkl')
    return df

#######################df costs and ledger
def export_ladger_get_costs(df):
    
    df_costs = df.copy()
    def fetch_prices_and_update_df(df_costs, df_close):
        # Function to decide which date to use
        def choose_date(row):
            if pd.notna(row['DateTrans']):
                return row['DateTrans']
            else:
                return row['StartDate']
        
        # Apply the function to choose the date and fetch the stock price or assign 0
        df_costs['price_on_trans'] = df_costs.apply(
            lambda row: 0 if row['units_hold'] == 0 else fetch_stock_price_on_date_close(row['Stock'], choose_date(row), df_close), 
            axis=1
        )
        
        # Calculate value_hold based on units_hold or units_updts
        def calculate_value_hold(row):
            if pd.notna(row['units_hold']):
                return row['units_hold'] * row['price_on_trans']
            elif pd.notna(row['units_updts']):  # Fallback if units_hold is NaN
                return row['units_updts'] * row['price_on_trans']
            else:
                return 0  # Return 0 if both units_hold and units_updts are NaN
    
        df_costs['amount'] = df_costs.apply(calculate_value_hold, axis=1)
    
        # Make all amount values positive
        df_costs['net_amount'] = df_costs['amount'].abs()
    
        # Determine the transaction type
        def determine_trans_type(row):
            if pd.notna(row['StartDate']) and row['units_hold'] > 0:
                return 'init'
            elif row['units_updts'] < 0:
                return 'sell'
            elif row['units_updts'] > 0:
                return 'buy'
            else:
                return 'init_added'
    
        df_costs['trans_type'] = df_costs.apply(determine_trans_type, axis=1)
    
        return df_costs
    
    
    df_costs_updated = fetch_prices_and_update_df(df_costs, df_close)
    ############
    # # Define a custom sorting key where 'init' has the highest priority, followed by 'sell' and 'buy' sorted by date, and then 'none'
    # def sort_priority(row):
    #     if row['trans_type'] == 'init':
    #         return (0, row['DateTrans'])  # 'init' gets the highest priority
    #     elif row['trans_type'] in ['sell', 'buy']:
    #         return (1, row['DateTrans'])  # 'sell' and 'buy' are second priority, sorted by date
    #     else:
    #         return (2, pd.Timestamp.max)  # Other types like 'none' get the lowest priority
    
    # # Apply the custom sorting function and sort the DataFrame
    # df_costs_updated['sort_priority'] = df_costs_updated.apply(sort_priority, axis=1)
    # df_costs_updated = df_costs_updated.sort_values(by='sort_priority')
    
    # # Drop the 'sort_priority' column if it's no longer needed
    # df_costs_updated.drop('sort_priority', axis=1, inplace=True)
    
    ########### DATES
    df_costs_updated['init_trans_dates'] = df_costs_updated['StartDate'].combine_first(df_costs_updated['DateTrans'])
    
    # Check if there are any rows where both StartDate and DateTrans are NaN and print an error if found
    if df_costs_updated['init_trans_dates'].isna().any():
        print("Error: Some entries have NaN in both StartDate and DateTrans.")
    
    ######## TRANS FEES
    
    # Calculate trans_fee based on the condition specified, adjusting for net_amount = 0
    df_costs_updated['trans_fee'] = df_costs_updated['net_amount'].apply(
        lambda x: 0 if x == 0 else (x * 0.0009 if x > 7334 else 6.60)
    )
    
    # Filter out rows where price_on_trans, amount, and net_amount are all zero
    # df_costs_updated = df_costs_updated[~((df_costs_updated['price_on_trans'] == 0) & 
    #                                       (df_costs_updated['amount'] == 0) & 
    #                                       (df_costs_updated['net_amount'] == 0))]
    
    
    ########### FIND PERIOD 
    
    # Ensure init_trans_dates is in datetime format
    df_costs_updated['init_trans_dates'] = pd.to_datetime(df_costs_updated['init_trans_dates'])
    
    # Get the current date
    current_date = datetime.now()
    
    # Calculate the difference in months and assign it to the 'period' column
    df_costs_updated['period'] = ((current_date.year - df_costs_updated['init_trans_dates'].dt.year) * 12 + 
                                   current_date.month - df_costs_updated['init_trans_dates'].dt.month)
    
    
    ################ write table !!! 
    df_costs_updated.to_pickle('_1_tables/_df_costs_1_2_complete_LEDGER.pkl')
    print('\n ATTN !! _22_ LEDGER EXPORTED _df_costs_1_2_complete_LEDGER.pkl\n')
    
    ############### GET aggregated table by trans_fee
    
    df_aggregated = df_costs_updated.groupby('period')['trans_fee'].sum().reset_index()
    
    # Identify the maximum period to ensure all periods are accounted for
    max_period = df_costs_updated['period'].max()
    
    # Create a DataFrame for all possible periods
    all_periods = pd.DataFrame({'period': range(max_period + 1)})
    
    # Merge with the aggregated data, filling missing periods with 0 for trans_fee
    df_cost_periods = all_periods.merge(df_aggregated, on='period', how='left').fillna(0)
    
    # Optional: convert trans_fee to integer if necessary
    df_cost_periods['trans_fee'] = df_cost_periods['trans_fee'].astype(int)
    
    df_cost_periods.to_pickle('_1_tables/_df_costs_1_3_br_costs.pkl')

    return df_cost_periods





####################
####################
####################
####################
####################
###################
def create_master_df(df, start_date_str):

    def get_cutoff_date():
        today = pd.Timestamp('today')
        while True:
            choice = input("Type 'cd' for today's date or 'pd' for the past adjusted date or the last day of the month: ")
        
            if choice.lower() == 'cd':
                return today.strftime('%Y-%m-%d')
            elif choice.lower() == 'pd':
                months_ago = int(input("Enter the number of months ago: "))
                first_day_of_next_month = today.replace(day=1) + pd.DateOffset(months=1)
                last_day_of_this_month = first_day_of_next_month - pd.DateOffset(days=1)
                last_day_of_past_month = (last_day_of_this_month - pd.DateOffset(months=months_ago)).strftime('%Y-%m-%d')
                return last_day_of_past_month
            else:
                print("Invalid choice. Please type 'cd' or 'pd'.")


    
    # Example usage
    cutoff_date_custom = get_cutoff_date()
    print("Selected cutoff date:", cutoff_date_custom)

    
    
    
    start_date = pd.to_datetime(start_date_str)
    today = pd.Timestamp(cutoff_date_custom) #pd.Timestamp('today')
    print(today)
    # Calculate the number of months from the start date to now
    total_months = (today.year - start_date.year) * 12 + today.month - start_date.month
    
    # List to hold each DataFrame slice
    df_list = []
    
    # Generate DataFrames from now going back to the start date
    for months_back in range(total_months + 1):
        temp_df = filter_df_by_months_and_analysis_dates_and_DIVS(df, months_back, 'StartDate',cutoff_date_custom) #### imp
        temp_df = temp_df.copy()  # Make a copy to safely modify the DataFrame
        temp_df.loc[:, 'period'] = months_back  # Use .loc to set the 'period' column
        df_list.append(temp_df)
        
        # Check if we have reached or exceeded the start date limit
        if (today - pd.DateOffset(months=months_back)).date() < start_date.date():
            break
    
    # Concatenate all DataFrames into a master DataFrame
    df_master = pd.concat(df_list, ignore_index=True)
    return df_master


##################
##################

exec(open(f"_12_a_DIV_CASH_RET_tables_.py",encoding="utf-8").read())



################
#####################  GRAPHS 
df_final = get_units_percentages(df)





