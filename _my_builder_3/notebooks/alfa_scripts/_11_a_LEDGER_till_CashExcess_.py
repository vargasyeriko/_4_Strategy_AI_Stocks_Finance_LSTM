df_cash_ledger = pd.DataFrame()
total_len_trans = len(df_add)
# ############################################################################
#Convert the 'TransDate' column to datetime format if it's not already
df_add['DateTrans'] = pd.to_datetime(df_add['DateTrans'])

# Now that 'TransDate' is guaranteed to be in datetime format, format it to a string
df_add['DateTrans'] = df_add['DateTrans'].dt.strftime('%Y-%m-%d')

############################################################################
print('\n**********************************************************************')
print(' \n SECTION_1 ::: UPDATING PORTFOLIO -> STOCK-to-STOCK EXCHANGES  ::: ')
print('**********************************************************************\n')
# Assuming df_add is your existing DataFrame
original_df_add = df_add.copy()  # Make a copy to avoid modifying the original DataFrame

for i in range(len(original_df_add)):
    # Select the i-th row and ensure it's a DataFrame
    df_add = original_df_add.iloc[[i]].copy()

    ############################################################################
    def calculate_transaction(hold_units_at_init, stock, trans_date, trans_type, percentage):
        """
        Calculates a transaction based on the initial units held and the other transaction inputs.
        Includes transaction fee calculation based on the transaction amount.
        """
        stock_price_at_trans = fetch_stock_price_on_date_close(stock, trans_date, df_close)
        #print(stock_price_at_trans)

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

        return df_transaction['trans_units'][0] , df_transaction['net_cash'][0],df_transaction['trans_fee'][0],df_transaction['trans_amount'][0]

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

################################
    def buy_stocks(ids, stocks, percents, amounts, dates):
        transactions = pd.DataFrame()  # Start with an empty DataFrame
    
        for id, stock_list, percent_list, amount, date in zip(ids, stocks, percents, amounts, dates):
            for stock, percent in zip(stock_list, percent_list):
                stock_price = fetch_stock_price_on_date_close(stock, trans_date, df_close)
                if stock_price is not None:
                    money_allocated = amount * (percent / 100)
                    trans_fee = money_allocated * 0.0009 if money_allocated > 7334 else 6.60
                    money_allocated_trans_fee = money_allocated - trans_fee
                    units_bought = money_allocated_trans_fee / stock_price
    
                    # Create a DataFrame for this transaction
                    transaction_df = pd.DataFrame({
                        "Stock": [stock],
                        "Amount Bought": [money_allocated_trans_fee],
                        'keep_drop': ['d'],
                        'trans_type': ['b'],
                        "DateTrans": [date],
                        "id_time": [id],
                        "id_time_buy": [id + 'b_' + stock],
                        "Stock Price": [stock_price],
                        "units_acquired": [units_bought],
                        "trans_fee": [trans_fee],
                        "Amount Bought_no_tf": [money_allocated]
                    })
    
                    # Concatenate this transaction DataFrame to the transactions DataFrame
                    transactions = pd.concat([transactions, transaction_df], ignore_index=True)
    
        return transactions

    stocks_sell   = df_add['exchange_stocks'].tolist()

    percents_sell = df_add['sell_perc'].tolist()

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
    ############################################################################
    ############################################################################
    df_to_trim_cash = df_buy.copy()
    df_stock_to_cash_ledger = df_to_trim_cash[df_to_trim_cash['Stock'] == 'CASH']
    
    df_cash_ledger = pd.concat([df_cash_ledger, df_stock_to_cash_ledger], ignore_index=True).sort_values(by='DateTrans').reset_index(drop=True)

    
    # Creating df_no_cash with rows where Stock does not equal 'CASH'
    df_buy = df_buy[df_buy['Stock'] != 'CASH'].copy()
    df = df[df['Stock'] != 'CASH'].copy()
    print()
    ############################################################################
    name = f"_0{i+1}_df_sell_{last_cutoff_date_str}.pkl"
    file_path = f"_21_add_ledger_sell/{name}"
    
    # Save DataFrame as pickle
    df_add.to_pickle(file_path)
    
    name = f"_0{i+1}_df_buy_{last_cutoff_date_str}.pkl"
    file_path = f"_22_add_ledger_buy/{name}"
    
    # Save DataFrame as pickle
    df_buy.to_pickle(file_path)

    ############################################################################ 
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
# ############################################################################*****************
# ############################################################################*****************
df_master_unit_updt = df.copy()
df = pd.DataFrame()        # Re start
# FIX DATES
df_master_unit_updt['StartDate_when_adding'] = df_master_unit_updt['StartDate'].copy()
# Now set all 'StartDate' entries to '2022-07-01'
df_master_unit_updt['StartDate'] = d_start_date
#df_master_unit_updt = df_master_unit_updt[df_master_unit_updt['Stock'] != 'CASH'].copy()
#
# FOR THE FIRST BIG ITERATION WRITE THIs FILE RIGHT AWAY!
df_master_unit_updt.to_pickle(f'_1_tables/{df_name_units_updt}.pkl')
# ############################################################################*****************
# ############################################################################*****************
# ############################################################################*****************
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
# ############################################################################*****************

stock_names = df_master_unit_updt['Stock']#[:-2].tolist()
df_all_sell = sum_units_sold_by_stock_sold(df_sell, stock_names)
df_all_buy =  sum_units_sold_by_stock_bought(df_buy, stock_names)
df_sum = sum_buy_sell_ordered(df_all_buy, df_all_sell)
###########################################################################
df_all = pd.merge(df_master_unit_updt, df_sum, on='Stock', how='inner')
df_all['hold_units_CHECK'] = df_all['hold_units_at_init_day_1'] + df_all['Total Units Bought'] + df_all['Total Units Sold']
############################################################################# Set display options
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)        # Use maximum width of the console
pd.set_option('display.max_colwidth', 20)   # Set maximum column width (can adjust as needed)
pd.set_option('display.expand_frame_repr', True)  # Expand the DataFrame representation to stretch across multiple lines
#pd.set_option('display.float_format', '{:.2f}'.format)  # Format floating points to show two decimal places
#TABLE MODIFICATIONS
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


selected_columns = [
    'Stock',   'StartDate', 'Transaction Fee (AUD)',
    'hold_units_at_init_day_1', 'hold_units_at_init', 'hold_units_CHECK']

# Create the new DataFrame with only the selected columns ALL
df_show = df_all[selected_columns]
############################################################################
############################################################################
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
############################################################################################ ::: INIT
# INIT =  df_updt : previous df_all (with sums) previous was df and virgin init portfolio_df
# #

columns_to_keep = ['Stock', 'StartDate']
# Columns you want to rename, specified as {'old_name': 'new_name'}
columns_to_rename = {
    'hold_units_at_init_day_1': 'units_hold'}

# First, select all the columns (both to keep and to rename)
all_columns = columns_to_keep + list(columns_to_rename.keys())
df_init_4_cash = df_updt[all_columns]

# Then, rename the specified columns
df_init_4_cash = df_init_4_cash.rename(columns=columns_to_rename)            
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
############################################################################################ ::: MERGE and SHOWCASE       df 
#### df = df_init_4_cash.append(df_sell_4_cash, ignore_index=True)
#### df = df.append(df_buy_4_cash, ignore_index=True)
df = pd.concat([df_init_4_cash, df_sell_4_cash, df_buy_4_cash], ignore_index=True) # concat
df = df.sort_values(by=['Stock', 'StartDate', 'DateTrans']) # SORT
# restart the dfs
df_init_4_cash = pd.DataFrame()
df_sell_4_cash = pd.DataFrame()
df_buy_4_cash = pd.DataFrame()
#print('\n-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_' )
print(f'\nSTATUS FOR ith ITERATION for the ith cut-off date :\n',
      f'\n * LENGTH of grand TOTAL transactions SELL * \t -> {len(df_sell)} ',
      f'\n * LENGTH of grand TOTAL transactions BUY * \t -> {len(df_buy)} ',
      f'\n   LENGTH of total of STOCKS in PORTFOLIO \t -> {len(df_master_unit_updt)}',
      f'\n   LENGTH all individual LEDGER transactions \t -> {len(df)} ')
# ############################################################################
# ############################################################################
### CASH BAL
# Display the updated df_updt DataFrame
pd.set_option('display.max_colwidth', None)
trans_cost_all_but_cash_stock_buys = df_updt['Transaction Fee (AUD)'].sum() # cashete
#print('************************ CASH **************************** ')
########################################################## ADD CASH BALANCE TABLE ####
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
        
        closing_price = fetch_stock_price_on_date_close(stock, trans_date, df_close)
        
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
# (1) GET STOCK x CASH : df_cash_bal
# Creating df_cash with rows where Stock equals 'CASH'
df_stock_to_cash_ledger = df_cash_ledger.copy()
    
# Create a new DataFrame df_cash_bal with selected columns and rename 'Amount Bought_no_tf' to 'amount'
df_cash_bal = df_stock_to_cash_ledger[['Amount Bought_no_tf', 'DateTrans']].copy()
df_cash_bal.rename(columns={'Amount Bought_no_tf': 'amount'}, inplace=True)
df_cash_bal['id_time_buy'] = df_stock_to_cash_ledger['id_time_buy'].copy()
df_cash_bal['trans_type'] = 'stock_to_cash'

###################################################################### (1_2) WRITE ledger to pkl
# WRITE out
name_df_stock_to_cash_ledger= f'_2_0_on_{last_cutoff_date_str}_trans_{total_len_trans}_over_{df_add_original_lenght}_tot_' #namee
#
df_cash_bal.to_pickle(f'_20_add_cash/{name_df_stock_to_cash_ledger}.pkl')
#print(f'\n...excess_updt_{last_cutoff_date_str}.pkl added to ledger Stock-x-Cash')  
#
###################################################################### (2) READ CASH INIT : df_cash_init
name_cash_init        = '_df_cash_init_0_init_CASH'
df_cash_init          = pd.read_pickle(f'_20_add_cash/{name_cash_init}.pkl')

###################################################################### (3) READ CASH INIT EMPTY modif: df_cash_init
name_cash_init_modif  = '_df_cash_init_1_empty_CASH'
df_cash_init_empty    = pd.read_pickle(f'_20_add_cash/{name_cash_init_modif}.pkl')
# ############################################################################
# ############################################################################ COCNAT (1) & (2)
# df_cash_bal_init_ledger_updt
df_cash_bal = pd.concat([df_cash_bal, df_cash_init], ignore_index=True).sort_values(by='DateTrans').reset_index(drop=True) 
# ############################################################################ COCNAT (1)(2) & 3
#to the empty one, so thats your up to ledger df
df_cash_bal = pd.concat([df_cash_bal, df_cash_init_empty], ignore_index=True).sort_values(by='DateTrans').reset_index(drop=True)
# after stock to cash and cash init
# **************************** FILL EMPTY CASH INIT to be written 
df_cash_bal = df_cash_bal.drop_duplicates(subset='id_time_buy') ## GET RID OF ALL DUPLICATES
df_cash_bal.to_pickle(f'_20_add_cash/{name_cash_init_modif}.pkl')

#NEXT pass updated units from cash excess!!!!!!!!!!
############################################################################
#filter_cash_excess_check =1
if filter_cash_excess_check != 0:
    #print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n' )
    #print('EXCESS CASH DETECTED UPDATES /// PROCEDDING ...')
    df_div = to_df_div(df)
    #print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n' )
    #input('')
    # Looping through each row of the DataFrame
    for index, row in df_cash_x_stock_ads.iterrows():
        # Assigning the row's values to variables
        date_cash_to_stock = row['date_cash_to_stock']
        per_cash_to_stock = row['per_cash_to_stock']
        stock_from_cash = row['stock_from_cash']
        df_div['StartDate'] = pd.to_datetime(df_div['StartDate'])
        df_div['EndDate'] = pd.to_datetime(df_div['EndDate'])
        #input('')
        # Filter dates to find cash amount to be * percent (excess cash )
        filtered_df = analyze_dates(df_div, date_cash_to_stock )
        
        # Get the right dates 
        #filtered_df= compare_and_set_analysis_end_date(filtered_df)

        #
        #input('')
        # Calc Cash till date of buy stock from excess cash 
        filtered_df = calculate_and_add_dividends(filtered_df)

        
        
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
        print(f'{per_cash_to_stock}% of Total Excess $  :',buying_power.iloc[0] ,
             f'for units : ',df_cash_trans['units_updts'].to_string(index=False),
              f' to {stock_from_cash}' ,'\n')
              #,df_cash_trans['units_updts'].to_string(index=False),'\n')
        
        
        #print('\n' )        
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
        # Check if the stock name is not in the master DataFrame
        for index, row in df_stocks_add.iterrows():
            if row['Stock'] not in df_master_unit_updt['Stock'].values:
                # Update the template with actual data
                new_row_template['Stock'] = row['Stock']
                new_row_template['StartDate'] = row['DateTrans']
                new_row_template['hold_units_at_init_day_1'] = 0
                new_row_template['hold_units_at_init'] = 0
        
                # Append the new row to the master DataFrame using pd.concat
                df_master_unit_updt = pd.concat([df_master_unit_updt, pd.DataFrame([new_row_template])], ignore_index=True)
        
                # Update existing stock units
                df_master_unit_updt.loc[df_master_unit_updt['Stock'] == row['Stock'],
                'hold_units_at_init'] += row['units_acquired']
            else:
                # DONT initialize just ::: Update existing stock units
                df_master_unit_updt.loc[df_master_unit_updt['Stock'] == row['Stock'], 
                'hold_units_at_init'] += row['units_acquired']
        
        
        ######## date
        df_master_unit_updt['StartDate_when_adding'] = df_master_unit_updt['StartDate'].copy()
        # Now set all 'StartDate' entries to '2022-07-01'
        df_master_unit_updt['StartDate'] = d_start_date
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
        
        #df_cash_bal = df_cash_bal.append(df_cash_add, ignore_index=True)
        df_cash_bal = pd.concat([df_cash_bal, df_cash_add], ignore_index=True)
        #print('>>> $ >>> $ >>> Updated CASH BAL table >>> $ >>> $ \n')
        print(df_cash_bal[['amount', 'id_time_buy']])
        print('-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ CASH_BAL UPDATED ! ' )
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
else:
    print('\nmoving on , no excess cash updates ')