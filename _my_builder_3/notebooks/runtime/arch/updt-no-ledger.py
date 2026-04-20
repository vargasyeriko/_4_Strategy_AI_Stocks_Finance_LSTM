
#############################################################################################

from _fns import sum_units_sold_by_stock_bought,sum_units_sold_by_stock_sold,sum_buy_sell_ordered
import pandas as pd
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import os
import glob
#

df_cash_ledger = pd.DataFrame()
total_len_trans = len(df_add)

# Get the current date and time
#
now = datetime.now();formatted_date_time = now.strftime("%Y_%m_%d_h%Hm%M");formatted_date_time


######################################################## df IMP- UNITS
df_master_unit_updt = df.copy()
df = pd.DataFrame()               # Re start
# FIX DATES
df_master_unit_updt['StartDate_when_adding'] = df_master_unit_updt['StartDate'].copy()
# Now set all 'StartDate' entries to '2022-07-01'
df_master_unit_updt['StartDate'] = d_start_date
#df_master_unit_updt = df_master_unit_updt[df_master_unit_updt['Stock'] != 'CASH'].copy()

# ##############################################################*****************
# ############################################################*****************
# ###############################################################*****************
import pandas as pd
import os
# GET df_sell & df_buy from folders
def merge_pickles(folder_path):
    merged_df = pd.DataFrame()
    for file in os.listdir(folder_path):
        if file.endswith('.pkl'):
            file_path = os.path.join(folder_path, file)
            df_append = pd.read_pickle(file_path)
            merged_df = merged_df.append(df_append, ignore_index=True)
    return merged_df


df_sell = merge_pickles('_21_add_ledger_sell')
df_buy = merge_pickles('_22_add_ledger_buy')

# ##############################################################*****************
# ############################################################*****************
# ###############################################################*****************

stock_names = df_master_unit_updt['Stock']#[:-2].tolist()
df_all_sell = sum_units_sold_by_stock_sold(df_sell, stock_names)
df_all_buy =  sum_units_sold_by_stock_bought(df_buy, stock_names)
df_sum = sum_buy_sell_ordered(df_all_buy, df_all_sell)

############################################################################
###########################################################################
df_all = pd.merge(df_master_unit_updt, df_sum, on='Stock', how='inner')
df_all['hold_units_CHECK'] = df_all['hold_units_at_init_day_1'] + df_all['Total Units Bought'] + df_all['Total Units Sold']
# # ############################################################################
# # ############################################################################

# Set display options
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)        # Use maximum width of the console
pd.set_option('display.max_colwidth', 20)   # Set maximum column width (can adjust as needed)
pd.set_option('display.expand_frame_repr', True)  # Expand the DataFrame representation to stretch across multiple lines



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





# ############################################################################
# Select the desired columns to keep in a new DataFrame
selected_columns = [
    'Stock',   'StartDate', 'Transaction Fee (AUD)',
    'hold_units_at_init_day_1', 'hold_units_at_init', 'hold_units_CHECK'
]

# Create the new DataFrame with only the selected columns ALL
df_show = df_all[selected_columns]
############################################################################
############################################################################

########################################################################  ::: SELL

#
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
############################################################################################ ::: INIT
# INIT =  df_updt : previous df_all (with sums) previous was df and virgin init portfolio_df
# #


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

####################################################
# if start_done == 'yes':
#     df_init_4_cash['NewColumn'] = 0
#     print('000')
# else:
#     print('ddddddd')
####################################################        
    
    
############################################################################################ ::: BUY
# BUY = df_buy
#
# #
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
############################################################################################ ::: 


df = pd.concat([df_init_4_cash, df_sell_4_cash, df_buy_4_cash], ignore_index=True) # concat
df = df.sort_values(by=['Stock', 'StartDate', 'DateTrans']) # SORT

#exec(open(f"_1_a_CASH_Excess_.py",encoding="utf-8").read()) #paths

print(len(df))





########################################################## ADD CASH BALANCE TABLE ####

import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_stock_price_on_date(stock_symbol, date):
    """
    Fetches the closing price of a stock on a specific date using yfinance.
    Expands the search range to accommodate for weekends and holidays.
    """
    try:
        start_date = (datetime.strptime(date, "%Y-%m-%d") - pd.Timedelta(days=2)).strftime("%Y-%m-%d")
        end_date = (datetime.strptime(date, "%Y-%m-%d") + pd.Timedelta(days=2)).strftime("%Y-%m-%d")
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
        
        if not stock_data.empty:
            if date in stock_data.index.strftime("%Y-%m-%d").tolist():
                return stock_data.loc[date]['Close']
            else:
                return stock_data['Close'].iloc[0]
    except Exception as e:
        print(f"Error fetching data for {stock_symbol} on {date}: {e}")
    return None

def calculate_units_with_transaction_fee(df):
    """
    Calculates the number of units that can be bought for each stock listed in the DataFrame,
    accounting for transaction fees.
    """
    df['DateTrans'] = pd.to_datetime(df['DateTrans']).dt.strftime('%Y-%m-%d')
    df['buying_power'] = df['CASH'] * (df['Percent_buy'] / 100)
    
    # Calculate transaction fees
    transaction_fees = []
    for index, row in df.iterrows():
        amount = row['buying_power']
        if amount > 7334:
            fee = amount * 0.0009
        elif amount == 0.0:
            fee = 0.0
        else:
            fee = 6.60
        transaction_fees.append(fee)
    
    df['transaction_fee'] = transaction_fees
    df['cash_exchange'] = df['buying_power'] - df['transaction_fee']
    
    units_can_buy = []
    for index, row in df.iterrows():
        stock = row['Stock']
        date_trans = row['DateTrans']
        cash_exchange = row['cash_exchange']
        
        closing_price = fetch_stock_price_on_date(stock, date_trans)
        
        if closing_price:
            units = cash_exchange / closing_price
        else:
            units = 0
            print(f"No price data available for {stock} on {date_trans}")
        
        units_can_buy.append(units)
    
    df['units_updts'] = units_can_buy
    return df



print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_' )

print('\n**********************************************************************')
print(' \n SECTION_2 ::: UPDATING PORTFOLIO -> STOCK-CASH EXCESS ALLOCATIONS :::')
print('**********************************************************************\n')


# ############################################################################
# ############################################################################
# **********************_1_ CASH UPDATES ***************************** ')
# ############################################################################
# ############################################################################


import pandas as pd
name_cash_init_modif  = '_df_cash_init_1_empty_CASH'
df_cash_bal    = pd.read_pickle(f'_20_add_cash/{name_cash_init_modif}.pkl')

# ############################################################################
# ############################################################################

# NEXT pass updated units from cash excess!!!!!!!!!!

# ############################################################################
#filter_cash_excess_check =1
if filter_cash_excess_check != 0:
    #print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n' )
    #print('EXCESS CASH DETECTED UPDATES /// PROCEDDING ...')
    exec(open(f"_1_a_CASH_Excess_.py",encoding="utf-8").read()) #paths
    #print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n' )
    
    # Looping through each row of the DataFrame
    for index, row in df_cash_x_stock_ads.iterrows():
        # Assigning the row's values to variables
        date_cash_to_stock = row['date_cash_to_stock']
        per_cash_to_stock = row['per_cash_to_stock']
        stock_from_cash = row['stock_from_cash']

        # Filter dates to find cash amount to be * percent (excess cash )
        filtered_df = filter_df_by_date(df_div, date_cash_to_stock , 'StartDate')

        # Get the right dates 
        filtered_df= compare_and_set_analysis_end_date(filtered_df)

        # Calc Cash till date of buy stock from excess cash 
        filtered_df = calculate_and_add_dividends(filtered_df)
        filtered_df

        # TOTAL DIVIDENDS AT THE TIME OF BUYING 
        total_dividends = filtered_df['Dividends'].sum()
        #print('\n\n TOTAL DIV : ' ,total_dividends)
        print(f'\n TOTAL DIVIDENDS by \t{date_cash_to_stock}:' ,round(total_dividends,3))

        # ADD exising cash trans till date of buy with cash excess
        df_cash_trans_excess = df_cash_bal[df_cash_bal['DateTrans'] < date_cash_to_stock]
        #df_cash_trans_excess 

        history_cash = df_cash_trans_excess['amount'].sum()

        print(f'\n TOTAL CASH HOLDS by \t{date_cash_to_stock}:' ,round(history_cash,3),'\n')


        cash_standing_at_buy = total_dividends + history_cash

        print(f'TOTAL CASH including Dividends $  :',round(cash_standing_at_buy,3),'\n')
        #print('\n**********************************************************')
        
        # Assuming the DataFrame 'df' is already created with the correct columns
        data = {
            'CASH': [cash_standing_at_buy],
            'Percent_buy': [per_cash_to_stock],  # These percentages will be divided by 100 in the calculation
            'Stock': [stock_from_cash],
            'DateTrans': [date_cash_to_stock]  # Example dates
        }
        df_cash_trans = pd.DataFrame(data)

        #print(f'\n{df_cash_trans}')

        ### UPDATES

        ##################### the next uses pns from _1_CASH_and_DIV_updt

        # Calculate and print the updated DataFrame with units
        df_cash_trans = calculate_units_with_transaction_fee(df_cash_trans)

        df_cash_trans["id_time_buy"] = 'CASH_for_' + df_cash_trans["Stock"] + '_'  +df_cash_trans['DateTrans'] 
        id_cash_excess = 'CASH_for_' + df_cash_trans["Stock"] + '_'  +df_cash_trans['DateTrans']
        
        df_cash_trans["trans_type"] = 'cash_to_stock'
        df_cash_trans["cash_exchange"] = df_cash_trans["cash_exchange"]*(-1)
        # trans_fee_from_cash_add = round(stock_df['transaction_fee'].sum(), 2)

        buying_power = round(df_cash_trans['buying_power'],3).astype(str)
        print(f'\nAllocating {per_cash_to_stock}% of Total Excess $  :',buying_power.iloc[0] ,
             f'\t...to ... {stock_from_cash} ...\n\n')
        
        print(' -> CASH BALANCE UPDATED AFTER CASH EXCESS ITERATION\n' )        

        print(df_cash_trans[['units_updts']])
        
        
        ### 1 Pass what has been bought to bd
        # GEST ADDing stocks
        df_stocks_add = df_cash_trans[['Stock', 'DateTrans', 'units_updts']].copy()
        df_stocks_add
        #################
        ################
        df_stocks_add.rename(columns={'units_updts': 'units_acquired'}, inplace=True)
        name_ce = f'_from_CashE_{last_cutoff_date_str}-{stock_from_cash}'
        file_path = f"_22_add_ledger_buy/{name_ce}.pkl"
        df_stocks_add.to_pickle(file_path)
        
        
        ##############################################
        ############################################## FOR graphing purposes, read/write inv_units ..
        ##############################################
        
        # INITIALIZE THE NEW STOCK if it is not in there 
        new_row_template = {col: 0 for col in df_master_unit_updt.columns}
        new_row_template.update({'Stock': None, 'StartDate': None, 'hold_units_at_init': 0,
                                 'hold_units_at_init_day_1': 0})

        # Check if the stock name is not in the master DataFrame
        for index, row in df_stocks_add.iterrows():
            if row['Stock'] not in df_master_unit_updt['Stock'].values:
                # Update the template with actual data
                new_row_template['Stock'] = row['Stock']
                new_row_template['StartDate'] = row['DateTrans']
                new_row_template['hold_units_at_init_day_1'] = 0
                new_row_template['hold_units_at_init'] = 0

                # Append the new row to the master DataFrame
                df_master_unit_updt = df_master_unit_updt.append(new_row_template,
                                                                 ignore_index=True)
                # Update existing stock units
                df_master_unit_updt.loc[df_master_unit_updt['Stock'] == row['Stock'],
                'hold_units_at_init'] += row['units_acquired']    
            else :
                # DONT initialize just ::: Update existing stock units
                df_master_unit_updt.loc[df_master_unit_updt['Stock'] == row['Stock'],
                'hold_units_at_init'] += row['units_acquired']

        #####
        #
        #
        df_master_unit_updt.to_pickle(f'_1_tables/{df_name_units_updt}.pkl')
        #
        #
        #####
        ##############################################
        
        columns_to_keep = ['DateTrans','id_time_buy', 'trans_type',]

        # Columns you want to rename, specified as {'old_name': 'new_name'}
        columns_to_rename = {
            'cash_exchange':'amount',
            'transaction_fee': 'costs',
            #'hold_units_CHECK': 'NewHoldUnitsCheck'
        }

        # First, select all the columns (both to keep and to rename)
        all_columns = columns_to_keep + list(columns_to_rename.keys())

        df_cash_add = df_cash_trans[all_columns]

        # Then, rename the specified columns
        df_cash_add = df_cash_add.rename(columns=columns_to_rename)
        df_cash_add
        #Write CASH out df to be concatenated
        df_cash_bal.to_pickle(f'_20_add_cash/_cashE_on_{date_cash_to_stock}_{stock_from_cash}.pkl')
        
        df_cash_bal = df_cash_bal.append(df_cash_add, ignore_index=True)
        #df_cash_bal = pd.concat([df_cash_bal, df_cash_add], ignore_index=True)
        #print('>>> $ >>> $ >>> Updated CASH BAL table >>> $ >>> $ \n')
        print(df_cash_bal[['amount', 'id_time_buy']])
        print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ CASH BAL UPDATED ! \n ' )
        # print('\n**********************************************************************')
        # print(' \n SECTION_3 ::: UPDATING PORTFOLIO -> STOCK-to-CASH  ::: ')
        # print('**********************************************************************\n\n')
        #####
        #
        #
        df_cash_bal.to_pickle(f'_20_add_cash/_df_cash_init_1_empty_CASH.pkl') 
        #
        #
        #####
        
        
        
        #exec(open(f"_1_a_CASH_Excess_.py",encoding="utf-8").read()) #paths
else:
    print('\nmoving on , no excess cash updates ')


# # ############################################################################
# # ############################################################################

# # ############################################################################
# # ############################################################################

input('')