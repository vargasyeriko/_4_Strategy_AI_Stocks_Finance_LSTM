# uptd


import pandas as pd
# # Step 1: Flag rows where 'Stock' is either 'Cash' or 'trans_cost'
# df['is_target'] = df['Stock'].isin(['Cash', 'trans_cost'])

# # Step 2: Sort the DataFrame to move flagged rows to the bottom
# df = df.sort_values(by='is_target', ascending=True)

# # Step 3: Drop the temporary flag column
# df.drop('is_target', axis=1, inplace=True)

#print('df has been updatede with all ne added stocks after start date ')
portfolio_df_init =df
df['hold_units_at_init_day_1']= portfolio_df_init['hold_units_at_init']


# ############################################################################
# ############################################################################
# #cash = 90
#Convert the 'TransDate' column to datetime format if it's not already
df_add['DateTrans'] = pd.to_datetime(df_add['DateTrans'])

# Now that 'TransDate' is guaranteed to be in datetime format, format it to a string
df_add['DateTrans'] = df_add['DateTrans'].dt.strftime('%Y-%m-%d')

############################################################################
print('\n\n**********************************************************************')
print(' \n SECTION_1 ::: UPDATING PORTFOLIO -> Allocations of SELLS ::: ')
print('**********************************************************************\n\n')


############################################################################
import pandas as pd
import yfinance as yf
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

def calculate_transaction(hold_units_at_init, stock, trans_date, trans_type, percentage):
    """
    Calculates a transaction based on the initial units held and the other transaction inputs.
    Includes transaction fee calculation based on the transaction amount.
    """
    stock_price_at_trans = fetch_stock_price_on_date(stock, trans_date)

    if stock_price_at_trans is None:
        print(f"Could not fetch price for {stock} on the transaction date.")
        return None

    # Calculate transaction units based on percentage
    trans_units = hold_units_at_init * (percentage / 100.0)
    trans_amount = trans_units * stock_price_at_trans  # Calculate transaction amount based on current price

    if trans_type == 's':
        trans_units = -trans_units  # Negate units for sales

    # Calculate transaction fee
    trans_fee = trans_amount * 0.0009 if trans_amount > 7334 else 6.60

    transaction = {
        'Stock': stock,
        'trans_type': trans_type,
        'trans_date': trans_date,
        'stock_price_at_trans': stock_price_at_trans,
        'trans_units': trans_units,
        'trans_amount': trans_amount,
        'trans_fee': trans_fee,
    }

    df_transaction = pd.DataFrame([transaction])
    df_transaction['net_cash'] = df_transaction['trans_amount'][0] - df_transaction['trans_fee'][0]
    
    return df_transaction['trans_units'][0] , df_transaction['net_cash'][0], df_transaction['trans_fee'][0],df_transaction['trans_amount'][0]        

# ############################################################################
# ############################################################################
import pandas as pd

# Assuming df_add and df are your DataFrames and are already defined

for index, row in df_add.iterrows():
    stock_id = row['Stock']
    trans_date = row['DateTrans']
    trans_type = row['trans_type']
    percentage = row['PercentSold']
    ids_ = row['id_time']
    
    # Find 'hold_units_at_init' in df where 'Stock' matches 'stock_id'
    if stock_id in df['Stock'].values:
        # Assuming 'Stock' is the column in df to match with 'stock_id'
        # And assuming 'hold_units_at_init' is the column you're interested in from df
        hold_units_at_init_row = df.loc[df['Stock'] == stock_id, 'hold_units_at_init']
        hold_units_at_init = hold_units_at_init_row.iloc[0] if not hold_units_at_init_row.empty else None
    else:
        hold_units_at_init = None  # Default value if not found
    
    # Assuming you have a function calculate_transaction defined somewhere
    # Check if hold_units_at_init is found (not None) before calling
    if hold_units_at_init is not None:
        
        units_sold,add_to_cash, trans_fee_add,before_trans_fee = calculate_transaction(hold_units_at_init, stock_id, trans_date, trans_type, percentage)
        # CALCULATE NEW UNITS BALANCE
        unit_bal = hold_units_at_init + units_sold
        
        df_add.loc[df_add['id_time'] == ids_, 'buy_amount'] = add_to_cash
        df_add.loc[df_add['id_time'] == ids_, 'units_sold'] = units_sold # add a value to 
        df_add.loc[df_add['id_time'] == ids_, 'trans_fee'] = trans_fee_add # add a value to 

        df_add.loc[df_add['id_time'] == ids_, 'before_trans_fee'] = before_trans_fee # add a value to 

        
        print(f'\nUnits HOLDS:  \t {round(hold_units_at_init,3)} \nUnits SOLD:\t',round(units_sold,3),
              f" ... \t{stock_id} & value:",round(add_to_cash,3),'$' ,
              '\nUnits UPDATE:\t ',round(unit_bal,3))
        
        # IF UNIT BALANCE CHANGE go CHANGE it
        if unit_bal != hold_units_at_init:
            df.loc[df['Stock'] == stock_id, 'hold_units_at_init'] = unit_bal
            #print(f"\t\t\t... {stock_id} ...UNITS update: {round(unit_bal,3)}")
        
        
        
        
    # Print the transaction details
    #print(f"\t\t\t\t---------> ---------> --------->---------> Stock ID >>> {stock_id}, \n\t\t\t\tDateTrans: {trans_date}, \n\t\t\t\tTransaction Type: {trans_type}")


#print('\n\namounts split or not -> to buy',amounts_split)
print('\n\n**********************************************************************')
print(' \n SECTION_2 ::: UPDATING PORTFOLIO -> Allocations of BUYS :::')
print('**********************************************************************\n')

# # ############################################################################
# # ############################################################################

# # ############################################################################
# # ############################################################################
# import yfinance as yf
# import pandas as pd
# from datetime import datetime

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

def buy_stocks(ids, stocks, percents, amounts, dates):
    transactions = []
    
    for id, stock_list, percent_list, amount, date in zip(ids, stocks, percents, amounts, dates):
        for stock, percent in zip(stock_list, percent_list):
            stock_price = fetch_stock_price_on_date(stock, date)
            if stock_price is not None:
                money_allocated = amount * (percent / 100)
                
                trans_fee = money_allocated * 0.0009 if money_allocated > 7334 else 6.60
                
                money_allocated_trans_fee =  money_allocated -trans_fee
                
                # transactions COSTS
                
                
                units_bought = money_allocated_trans_fee / stock_price
                
                transactions.append({
                    "Stock": stock,
                    "Amount Bought":money_allocated_trans_fee,

                    'keep_drop': 'd',
                    'trans_type':'b',
                    "DateTrans": date,
                    "id_time": id,
                    "id_time_buy": id + 'b_'+ stock,
                    "Stock Price": stock_price,
                    "units_acquired": units_bought,
                    "trans_fee": trans_fee,
                    
                    "Amount Bought_no_tf": money_allocated
                })
    
    return pd.DataFrame(transactions)


stocks_sell   = df_add['exchange_stocks'].tolist()

percents_sell = df_add['sell_perc'].tolist()
import ast

# Assuming df_add['sell_perc'] contains strings that represent lists
percents_sell = df_add['sell_perc'].tolist()

# Convert the string representation of lists into actual lists
percents_sell = [ast.literal_eval(item) if isinstance(item, str) else item for item in percents_sell]

# Convert each item in each list to an integer
percents_sell = [[int(item) for item in sublist] for sublist in percents_sell]

amounts_split = df_add['buy_amount'].tolist()
dates_sell    = df_add['DateTrans'].tolist()
ids_sell      = df_add['id_time'].tolist()

    
# Example usage
ids = ids_sell
stocks = stocks_sell
percents = percents_sell
amounts = amounts_split
dates = dates_sell

df_buy = buy_stocks(ids, stocks, percents, amounts, dates)

df_buy


############################################################################ Write the cash bal out 
############################################################################
#last_date '23/23/23'
    
    
# # Creating df_cash with rows where Stock equals 'CASH'
# df_cash = df_buy[df_buy['Stock'] == 'CASH']
    
    
# # Create a new DataFrame df_cash_bal with selected columns and rename 'Amount Bought_no_tf' to 'amount'
# df_cash_bal = df_cash[['Amount Bought_no_tf', 'DateTrans']].copy()
# df_cash_bal.rename(columns={'Amount Bought_no_tf': 'amount'}, inplace=True)
# df_cash_bal['id_time_buy'] = df_cash['id_time_buy'].copy()
# df_cash_bal['trans_type'] = 'stock_to_cash'

# df_cash_bal.to_pickle(f'_20_add_cash/_2_0_df_cash_updt_{last_cutoff_date}.pkl') #cashete

# input('f_20_tables/_2_0_df_cash_updt_{last_cutoff_date}.pkl')
# ############################################################################
############################################################################ THE ONE THAT MODIFIES THE DF
    

df_to_trim_cash = df_buy.copy()    
# Creating df_no_cash with rows where Stock does not equal 'CASH'
df_buy = df_buy[df_buy['Stock'] != 'CASH'].copy()
df = df[df['Stock'] != 'CASH'].copy()
    
############################################################################
############################################################################ 
    

import pandas as pd

# Assuming df and df_buy are your DataFrames and are already defined

for index, row in df_buy.iterrows():
    stock_id = row['Stock']
    trans_date = row['DateTrans']
    trans_type = row['trans_type']
    id_time_b = row['id_time_buy']  # Assuming this is your unique transaction identifier

    # Find 'hold_units_at_init' in df where 'Stock' matches 'stock_id'
    if stock_id in df['Stock'].values:
        hold_units_at_init_row = df.loc[df['Stock'] == stock_id, 'hold_units_at_init']
        hold_units_at_init = hold_units_at_init_row.iloc[0] if not hold_units_at_init_row.empty else None
    else:
        hold_units_at_init = None  # Default value if not found

    # Check if hold_units_at_init is found (not None) before calling
    if hold_units_at_init is not None:
        # Calculate new units balance
        units_bought = row['units_acquired']  # Directly use the row value for units acquired
        unit_bal = hold_units_at_init + units_bought

        print(f'\nUnits HOLDS: \t{round(hold_units_at_init, 3)}, \nUnits BOUGHT: \t{round(units_bought, 3)}, \nUnits UPDATE: \t{round(unit_bal, 3)}',f' ...\t {stock_id} .')

        # If unit balance changes, go change it
        if unit_bal != hold_units_at_init:
            # Assuming you need to update the initial DataFrame 'df' with the new balance
            df.loc[df['Stock'] == stock_id, 'hold_units_at_init'] = unit_bal
            #print(f"\t\t\t... {stock_id} ... UNITS update: {round(unit_bal,3)}")

    # Print the transaction details
    #print(f"\t\t\t\t---------> Stock ID: {stock_id}, \n\t\t\t\tDateTrans: {trans_date}, \n\t\t\t\tTransaction Type: {trans_type}")

# ############################################################################
# ############################################################################

############################################################################
############################################################################  HERE EXPORT FOR UNIT UPDT final df ***********


# CHECK
print('\n\n final df upt dies')
############################################################################
############################################################################
stock_names = df['Stock']#[:-2].tolist()
df_all_sell = sum_units_sold_by_stock_sold(df_add, stock_names)
df_all_buy =  sum_units_sold_by_stock_bought(df_buy, stock_names)
df_sum = sum_buy_sell_ordered(df_all_buy, df_all_sell)
df_all = pd.merge(df, df_sum, on='Stock', how='inner')
df_all['hold_units_CHECK'] = df_all['hold_units_at_init_day_1'] + df_all['Total Units Bought'] + df_all['Total Units Sold']
# # ############################################################################
# # ############################################################################

# Set display options
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)        # Use maximum width of the console
pd.set_option('display.max_colwidth', 20)   # Set maximum column width (can adjust as needed)
pd.set_option('display.expand_frame_repr', True)  # Expand the DataFrame representation to stretch across multiple lines
#pd.set_option('display.float_format', '{:.2f}'.format)  # Format floating points to show two decimal places

#Assuming df_all is your DataFrame
#print(df_all)

# Assuming df_all is your DataFrame

# ############################################################################
# ############################################################################
# ## TABLE MODIFICATIONS

# # ############################################################################
# # ############################################################################


# TO DADD ::: 'Price Bought', 'Latest Price' # SELL
df_sell = df_add.copy()
# BUY' df_buy

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

# # Display the updated df_updt DataFrame
# pd.set_option('display.max_colwidth', None)
# trans_cost_all_but_cash_stock_buys = df_updt['Transaction Fee (AUD)'].sum() # cashete


# ############################################################################
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
#print(df_show)                  IMPpppppp
# ############################################################################
# ############################################################################

# # TILL HERE the most updates tables for 
# ########################################
# print('\n\nRE-ARRANGING - TABLES','\n\n**********************************************************')
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
# Now, df_all_se
############################################################################################  ::: SELL
# SELL = df_sell : previous was df_add
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
############################################################################################ ::: MERGE and SHOWCASE       df ends 
#print('\n',df_init_4_cash.head(1),'\n\n',df_sell_4_cash.head(1),'\n\n',df_buy_4_cash.head(1))
#
#
# SHOWCASE changes in df_show
#df = pd.DataFrame()
df = pd.concat([df_init_4_cash, df_sell_4_cash, df_buy_4_cash], ignore_index=True) # concat
df = df.sort_values(by=['Stock', 'StartDate', 'DateTrans']) # SORT
print(f'CONCAT head final :df_ledger \n\nLENGTH of trans in there {len(df_add)} // :: {df_add_original_lenght}','number_of stocks',(len(df)),'\n\n**********************************************************')
print('**********************************************************')

# ############################################################################
# ############################################################################
# **********************_1_ CASH and DIV ***************************** ')
# ############################################################################
# ############################################################################

# ############################################################################
# ############################################################################

# ############################################################################
# ############################################################################

### CASH BAL
    
# Display the updated df_updt DataFrame
pd.set_option('display.max_colwidth', None)
trans_cost_all_but_cash_stock_buys = df_updt['Transaction Fee (AUD)'].sum() # cashete
    
    
# cash % INIT
#cash_start_value = cash_start_value_d+cash_start_value_g
#
print('\n\n******************** DIV & CASH ************************** ')

# print('cash_start_value\t\t\t',round(cash_start_value,3),'\ntrans_cost_all_but_cash_stock_buys\t',
# round(trans_cost_all_but_cash_stock_buys,3))

#import pandas as pd

# Assuming df_cash is your existing DataFrame and it has the columns 'Amount Bought_no_tf' and 'DateTrans'


    
    
    
    
    
    
# # Create a new DataFrame df_cash_bal with selected columns and rename 'Amount Bought_no_tf' to 'amount'
# df_cash_bal = df_cash[['Amount Bought_no_tf', 'DateTrans']].copy()
# df_cash_bal.rename(columns={'Amount Bought_no_tf': 'amount'}, inplace=True)
# df_cash_bal['id_time_buy'] = df_cash['id_time_buy'].copy()
# df_cash_bal['trans_type'] = 'stock_to_cash'

# if 'costs' not in df_cash.columns:
#     # If not, add 'costs' column with all values set to 0
#     df_cash_bal['costs'] = 0
    
# Your df_cash_bal now contains the 'amount' and 'DateTrans' columns
#df_cash_bal
# CASH INIT

# Create a new row to append to df_cash_bal
# new_row = {
#     'amount': cash_start_value,  # Adding cash_start_value to amount
#     'DateTrans': d_start_date,  # Setting DateTrans to d_start_date
#     'id_time_buy': f'Def_init_INV_{d_start_date}',  # Setting id to 'Def_init_INV_{d_start_date}'
#     'trans_type': 'cash_init',  # Setting transaction type to 'cash_init'
#     'costs': 0  # Setting costs to 0
# }

# # Append the new row to df_cash_bal
# df_cash_bal = df_cash_bal.append(new_row, ignore_index=True)
# TRANS COSTS

# Create a new row to append to df_cash_bal
# new_row = {
#     'amount': 0,  # Adding cash_start_value to amount
#     'DateTrans':'start-end' , # Setting DateTrans to d_start_date
#     'id_time_buy': 'id_trans_cost_1' , # Setting id to 'Def_init_INV_{d_start_date}'
#     'trans_type': 'trans_cost_all_but_cash_stock_buys',  # Setting transaction type to 'cash_init'
#     'costs': trans_cost_all_but_cash_stock_buys  # Setting costs to 0
# }

# # Append the new row to df_cash_bal
# df_cash_bal = df_cash_bal.append(new_row, ignore_index=True)
# df_cash_bal

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
# **********************_1_ CASH and DIV a ***************************** ')
# ############################################################################
# ############################################################################

# ############################################################################
# ############################################################################

# ############################################################################
# ############################################################################
# #_1_a_ BUY FROM CASH
exec(open(f"_1_a_CASH_Excess_.py",encoding="utf-8").read()) #paths

import os

# ############################################################################
# ############################################################################
###################################################################### HERE IMPORT CASH cashete
# Creating df_cash with rows where Stock equals 'CASH'
df_stock_to_cash_ledger = df_to_trim_cash[df_to_trim_cash['Stock'] == 'CASH']
    
    
# Create a new DataFrame df_cash_bal with selected columns and rename 'Amount Bought_no_tf' to 'amount'
df_cash_bal = df_stock_to_cash_ledger[['Amount Bought_no_tf', 'DateTrans']].copy()
df_cash_bal.rename(columns={'Amount Bought_no_tf': 'amount'}, inplace=True)
df_cash_bal['id_time_buy'] = df_stock_to_cash_ledger['id_time_buy'].copy()
df_cash_bal['trans_type'] = 'stock_to_cash'

#f_cash_bal.to_pickle(f'_20_add_cash/_2_0_df_cash_updt_{last_cutoff_date}.pkl') #cashete


# WRITE out
last_cutoff_date_str = last_cutoff_date.strftime('%Y-%m-%d')
name_df_stock_to_cash_ledger= f'\n\n_2_0_df_cash_updt_{last_cutoff_date_str}'
#
df_cash_bal.to_pickle(f'_20_add_cash/{name_df_stock_to_cash_ledger}.pkl')
print(f'\n...excess_updt_{last_cutoff_date_str}.pkl added to ledger Stock-x-Cash')  

# ############################################################################
# ############################################################################ COCNAT WITH INIT and hist STOCK_to_CASH hist
# List all pickle files in the directory


# Assuming df_cash_bal is already defined in your session, and you want to append all .pkl files from '_20_add_cash' directory

# Path to the directory containing the .pkl files
# directory = '_20_add_cash'

# # List all .pkl files in the specified directory
# pkl_files = [f for f in os.listdir(directory) if f.endswith('.pkl')]

# # Load each .pkl file and concatenate it with df_cash_bal
# for file_name in pkl_files:
#     file_path = os.path.join(directory, file_name)
#     data = pd.read_pickle(file_path)
#     df_cash_bal_init_ledger_updt = pd.concat([df_cash_bal, data], ignore_index=True)

    
    
    
# import pandas as pd
# import os

# # Assuming df_cash_bal is already defined in your session, and you want to append all .pkl files from '_20_add_cash' directory

# Path to the directory containing the .pkl files
directory = '_20_add_cash'

# List all .pkl files in the specified directory
pkl_files = [f for f in os.listdir(directory) if f.endswith('.pkl')]

# Load each .pkl file and append it to df_cash_bal
for file_name in pkl_files:
    file_path = os.path.join(directory, file_name)
    data_cash_updt = pd.read_pickle(file_path)
    df_cash_bal_init_ledger_updt = df_cash_bal.append(data_cash_updt, ignore_index=True)  
    
    
df_cash_bal_init_ledger_updt = df_cash_bal_init_ledger_updt.sort_values(by='DateTrans').reset_index(drop=True)    
    
print('\n\n',df_cash_bal_init_ledger_updt, '\n\n')


#df_cash_bal_init_ledger_updt.to_pickle(f'_20_add_cash/_0_updt_init_ledger/_0_updt_init_ledger.pkl')



#default_name = f'\n\n_2_0_df_cash_updt_{last_cutoff_date}.pkl'

# files = [f for f in os.listdir(directory) if f.endswith('.pkl')]

# # Initialize an empty DataFrame for concatenation if no files are found
# main_df = df_cash_bal

# # Load the DataFrame from 'cash_bal.pkl' if it exists
# if default_name in files:
#     df_cash_bal = pd.read_pickle(f"{directory}/{default_name}")
#     main_df = pd.concat([main_df, df_cash_bal], ignore_index=True)

# # Concatenate with other DataFrames if any
# for file in files:
#     if file != default_name:
#         df = pd.read_pickle(f"{directory}/{file}")
#         main_df = pd.concat([main_df, df], ignore_index=True)

# # Save or handle the concatenated DataFrame as needed
# print('\n\n>>> ALL CASH HISTORY till {date}\n\n',len(main_df))  # Print to see some of the c

# print(main_df)
#input('click to be done then another to start')


# df_cash = ''
# df_add = ''
# df_buy= ''
# df=''




# ############################################################################
# ############################################################################

# ############################################################################
# ############################################################################

# ############################################################################
# ############################################################################

# filter_cash_excess =1

# if filter_cash_excess != 0:
#     print('\nEXCESS CASH DETECTED UPDATES /// PROCEDDING ... \n')
#     print('**********************************************************')

    
#     # Looping through each row of the DataFrame
#     for index, row in df_cash_x_stock_ads.iterrows():
#         # Assigning the row's values to variables
#         date_cash_to_stock = row['date_cash_to_stock']
#         per_cash_to_stock = row['per_cash_to_stock']
#         stock_from_cash = row['stock_from_cash']

#         # Filter dates to find cash amount to be * percent (excess cash )
#         filtered_df = filter_df_by_date(df_div, date_cash_to_stock , 'StartDate')

#         # Get the right dates 
#         filtered_df= compare_and_set_analysis_end_date(filtered_df)

#         # Calc Cash till date of buy stock from excess cash 
#         filtered_df = calculate_and_add_dividends(filtered_df)
#         filtered_df

#         # TOTAL DIVIDENDS AT THE TIME OF BUYING 
#         total_dividends = filtered_df['Dividends'].sum()
#         #print('\n\n TOTAL DIV : ' ,total_dividends)
#         print(f'\n TOTAL DIVIDENDS by \t{date_cash_to_stock}:' ,round(total_dividends,3))

#         # ADD exising cash trans till date of buy with cash excess
#         df_cash_trans_excess = df_cash_bal[df_cash_bal['DateTrans'] < date_cash_to_stock]
#         df_cash_trans_excess 

#         history_cash = df_cash_trans_excess['amount'].sum()

#         print(f'\n TOTAL CASH HOLDS by \t{date_cash_to_stock}:' ,round(history_cash,3),'\n')


#         cash_standing_at_buy = total_dividends + history_cash

#         print(f'TOTAL CASH including Dividends $  :',round(cash_standing_at_buy,3))

#         # Assuming the DataFrame 'df' is already created with the correct columns
#         data = {
#             'CASH': [cash_standing_at_buy],
#             'Percent_buy': [per_cash_to_stock],  # These percentages will be divided by 100 in the calculation
#             'Stock': [stock_from_cash],
#             'DateTrans': [date_cash_to_stock]  # Example dates
#         }
#         df_cash_trans = pd.DataFrame(data)

#         #print(f'\n{df_cash_trans}')

#         ### UPDATES

#         ##################### the next uses pns from _1_CASH_and_DIV_updt

#         # Calculate and print the updated DataFrame with units
#         df_cash_trans = calculate_units_with_transaction_fee(df_cash_trans)

#         df_cash_trans["id_time_buy"] = 'CASH_for_' + df_cash_trans["Stock"] + '_'  +df_cash_trans['DateTrans'] 
#         df_cash_trans["trans_type"] = 'cash_to_stock'
#         df_cash_trans["cash_exchange"] = df_cash_trans["cash_exchange"]*(-1)
#         # trans_fee_from_cash_add = round(stock_df['transaction_fee'].sum(), 2)

#         buying_power = round(df_cash_trans['buying_power'],3).astype(str)
#         print(f'\nAllocating {per_cash_to_stock}% of Total Excess $  :',buying_power.iloc[0] ,
#              f'\t ... to ... {stock_from_cash} ...\n\n')

#         ### 1 Pass what has been bought to bd
#         # GEST ADDing stocks
#         df_stocks_add = df_cash_trans[['Stock', 'DateTrans', 'units_updts']]
#         df_stocks_add

#         #CONCAT all together 
#         df = pd.concat([df, df_stocks_add], ignore_index=True)
#         df =  df.sort_values(by='Stock').reset_index(drop=True)
#         df

#         columns_to_keep = ['DateTrans','id_time_buy', 'trans_type',]

#         # Columns you want to rename, specified as {'old_name': 'new_name'}
#         columns_to_rename = {
#             'cash_exchange':'amount',
#             'transaction_fee': 'costs',
#             #'hold_units_CHECK': 'NewHoldUnitsCheck'
#         }

#         # First, select all the columns (both to keep and to rename)
#         all_columns = columns_to_keep + list(columns_to_rename.keys())

#         df_cash_add = df_cash_trans[all_columns]

#         # Then, rename the specified columns
#         df_cash_add = df_cash_add.rename(columns=columns_to_rename)
#         df_cash_add

#         df_cash_bal = pd.concat([df_cash_bal, df_cash_add], ignore_index=True)
#         print(df_cash_bal[['amount', 'id_time_buy', 'costs']])
#         exec(open(f"_1_a_CASH_Excess_.py",encoding="utf-8").read()) #paths
# else:
#     print('\nmoving on , no excess cash updates ')



# # ############################################################################
# # ############################################################################
# # **********************_1_ CASH and DIV ***************************** ')
# # ############################################################################
# # ############################################################################

# # ############################################################################
# # ############################################################################

# # ############################################################################
# # ############################################################################




# # ############################################################################
# # ############################################################################

# # ############################################################################
# # ############################################################################

# # ############################################################################
# # ############################################################################

# # ############################################################################
# # ############################################################################

