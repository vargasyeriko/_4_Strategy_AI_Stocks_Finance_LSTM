def update_stock_list():
    directory = '_1_fetch/stock_list'
    # Get the list of all files in the directory
    files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.pkl')]
    
    # If no files are found, return an empty list and print a message
    if not files:
        print("No files found in the directory.")
        return [], []

    # Find the most recent file based on the modification time
    latest_file = max(files, key=os.path.getmtime)

    # Read the DataFrame from the pickle file
    df = pd.read_pickle(latest_file)

    # Extract the 'Stock' column into a list
    l_stock_list_newest_processed = df['Stock'].tolist()

    # Assuming l_stocks_updt is defined elsewhere and accessible
    global l_stocks_updt

    # Find stocks in l_stocks_updt not in l_stock_list_newest_processed
    _new_stocks = [stock for stock in l_stocks_updt if stock not in l_stock_list_newest_processed]
    # Check if there are new stocks to add
    if not _new_stocks:
        print("No new stocks to add.\n")
    else:
        print("New Stocks:", _new_stocks)
        main_stock_table_fetched(l_stocks_updt, d_start_date)
        fetch_dividend_analysis(l_stocks_updt, d_start_date)

    return l_stock_list_newest_processed, _new_stocks

#newest_processed, _new_stocks = update_stock_list(directory)
##############################################################################################
##############################################################################################
# _#_FN NAME ****** 9999 <<<      - sum units sold by stock -        >>> 9999 **********
############################ *********************************** #############################
######################################### - - - ##############################################

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


##############################################################################################
##############################################################################################
# _#_FN NAME ****** 9999 <<<      - sum units sold by stock -        >>> 9999 **********
############################ *********************************** #############################
######################################### - - - ##############################################

#
def generate_portfolio_allocations(total_investment, risk_profile):
    # Set default allocations
    allocations = {'Defensive': 0.5, 'Growth': 0.5}
    
    # Update allocations based on the risk profile
    if risk_profile == 'Moderate':
        allocations = {'Defensive': 0.7, 'Growth': 0.3}
    elif risk_profile == 'Balanced':
        allocations = {'Defensive': 0.5, 'Growth': 0.5}
    elif risk_profile == 'Balanced Growth':
        allocations = {'Defensive': 0.3, 'Growth': 0.7}
    elif risk_profile == 'Growth':
        allocations = {'Defensive': 0.2, 'Growth': 0.8}
    elif risk_profile == 'High Growth':
        allocations = {'Defensive': 0, 'Growth': 1}  # 100% Growth
    
    # Calculate the actual investment amounts based on the allocations
    investment_amounts = {key: value * total_investment for key, value in allocations.items()}
    return investment_amounts


def pick_profile():
    # Adjust the user input prompt and mapping to include the new options
    print("Please select your risk profile by entering the corresponding number:\n")
    print("1 - Moderate")
    print("2 - Balanced")
    print("3 - Balanced Growth")
    print("4 - Growth")
    print("5 - High Growth")
    risk_profile_number = int(input("\n\tEnter the number of your choice (1/2/3/4/5): "))

    # Map the numerical choice to a risk profile string
    if risk_profile_number == 1:
        risk_profile = 'Moderate'
    elif risk_profile_number == 2:
        risk_profile = 'Balanced'
    elif risk_profile_number == 3:
        risk_profile = 'Balanced Growth'
    elif risk_profile_number == 4:
        risk_profile = 'Growth'
    elif risk_profile_number == 5:
        risk_profile = 'High Growth'
    else:
        print("Invalid selection. Please restart and enter a valid number (1, 2, 3, 4, or 5).")
        exit()  # Exit or handle invalid input as necessary
    return risk_profile 

##############################################################################################
##############################################################################################
# _#_FN NAME ****** 9999 <<<      - sum units sold by stock -        >>> 9999 **********
############################ *********************************** #############################
######################################### - - - ##############################################
def calculate_investment_details(start_dates_list, stock_symbol, df_close):
    from datetime import datetime
    results = []  # Initialize an empty list to store results for each start date

    for start_date_str in start_dates_list:
        # Convert start date string to datetime object
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

        # Check if the start date is in the DataFrame's index
        if start_date in df_close.index:
            # Check if the stock symbol is in the DataFrame's columns
            if stock_symbol in df_close.columns:
                start_price = df_close.loc[start_date, stock_symbol]
                # Fetch the most recent stock data
                latest_price = df_close.iloc[-1][stock_symbol]

                results.append((start_price, latest_price))
            else:
                results.append((f"Stock symbol {stock_symbol} not found in DataFrame.",))
        else:
            results.append((f"Start date {start_date_str} not found in DataFrame.",))

    return results
#
######### END
##############################################################################################
##############################################################################################
# _#_FN NAME ****** 9999 <<<      - sum units sold by stock -        >>> 9999 **********
############################ *********************************** #############################
######################################### - - - ##############################################
def master_fetch_check(l_stocks_updt,d_start_date):
    
    # Load the DataFrame
    df_close = pd.read_pickle("_1_fetch/_0_fetched_stock_data_prices.pkl")
    
    # Ensure the index is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df_close.index):
        df_close.index = pd.to_datetime(df_close.index)
    
    # Check for the latest available date
    latest_date = df_close.index[-1]
    
    # Calculate the start date for the 30-day check
    start_check_date = latest_date - timedelta(days=30)
    
    # Check for any completely NaN rows in the last 30 days
    nan_in_last_30 = df_close.loc[start_check_date:latest_date].isna().all(axis=1).any()
    
    # Check if the latest date is today and if there's valid data
    if latest_date.date() != datetime.today().date() or nan_in_last_30:
        # Archive the current DataFrame if outdated or data is invalid
        df_close.to_pickle("_1_fetch/_0_fetched_stock_data_prices_OLD.pkl")
    
        # Calculate the gap in days
        days_since_last_fetch = (datetime.today().date() - latest_date.date()).days
    
        # Determine how many days to go back based on the gap
        if 0 <= days_since_last_fetch <= 25:
            fetch_days_back = 30
        elif 26 <= days_since_last_fetch <= 90:
            fetch_days_back = 120
        else:
            fetch_days_back = 180  # Adjust this as needed
    
        # Calculate the new start date
        d_start_date = latest_date - timedelta(days=fetch_days_back)
        
        # Run your function
        print('\n->', len(l_stocks_updt), f'Stocks being fetched from {d_start_date} till today')
       
        # UPDATE STOCKS
        main_stock_table_fetched(l_stocks_updt, d_start_date)
        # UPDATE DIVS
        fetch_dividend_analysis(l_stocks_updt, d_start_date)
        
        # Read the potentially updated data
        df_close = pd.read_pickle("_1_fetch/_0_fetched_stock_data_prices.pkl")
        
        # Check for NaN in the last row and fill with the previous day's data if necessary
        if df_close.iloc[-1].isnull().any():
            df_close.iloc[-1] = df_close.iloc[-2]
        
        # Read the old data
        df_old = pd.read_pickle("_1_fetch/_0_fetched_stock_data_prices_OLD.pkl")
        
        # Remove any rows in df_old that are in the new df_close
        df_old = df_old[~df_old.index.isin(df_close.index)]
        
        # Combine the old data with the new data
        df_final = pd.concat([df_old, df_close])
        
        # Save the combined DataFrame
        df_final.to_pickle("_1_fetch/_0_fetched_stock_data_prices.pkl")
    
        # Re-assign d_start_date
    else:
        print("\nATTN ! The last date in the DataFrame is today's date \nThe data is valid. No action needed & df_close imported")

        df_final = pd.read_pickle("_1_fetch/_0_fetched_stock_data_prices.pkl")
        # Ensure that the index is of datetime type if it isn't already
        if not pd.api.types.is_datetime64_any_dtype(df_final.index):
            df_final.index = pd.to_datetime(df_final.index)
            
        return df_final

##############################################################################################
##############################################################################################
# _#_FN NAME ****** 9999 <<<      - sum units sold by stock -        >>> 9999 **********
############################ *********************************** #############################
######################################### - - - ##############################################
#END
def _PORT_DEF_get():

    ### ############################################################################
    #print('\n -> DEFENSIVE')
    ### Start Dates -> they are 9 because of cash and trans_cost
    len_stocks_d = len(portfolio_labels_d)
    start_date = [d_start_date] * (len_stocks_d+2)
    
    ### Initial investments and portfolio setup
    portfolio_percentages = portfolio_percentages_d
    
    #print(portfolio_percentages)
    ############################################################################data_to_append_df_d
    df_columns = ['Stock', 'PercentSold', 'keep_drop', 'trans_type', 'DateTrans','exchange_stocks','sell_perc']
    hist_df_d = pd.DataFrame(columns=df_columns)  # Initialize with the updated columns
    
    
    hist_df_d = pd.concat([hist_df_d, data_to_append_df_d], ignore_index=True)
    
    # Ensure that all entries in 'exchange_stocks' and 'sell_perc' are lists of strings
    hist_df_d['exchange_stocks'] = hist_df_d['exchange_stocks'].apply(lambda lst: [str(item) for item in lst])
    hist_df_d['sell_perc'] = hist_df_d['sell_perc'].apply(lambda lst: [str(percentage) for percentage in lst])
    hist_df_d['id_time'] = hist_df_d['Stock'] + "_" + hist_df_d['DateTrans'] + "_" + hist_df_d['trans_type']
    
    initial_investment = initial_investment_D  # AUD
    #
    #print(f'\nInitial Investment is {initial_investment}')
    # Calculate the total percentage currently allocated to stocks
    total_percentage_allocated = sum(portfolio_percentages)
    cash_percentage = 1 - total_percentage_allocated  # Remaining percentage for cash
    
    # Update the portfolio to include cash
    portfolio_percentages.append(cash_percentage)
    portfolio_labels_d.append('Cash')
    
    # Calculate invested amounts including the cash component
    invested_amounts = [percentage * initial_investment for percentage in portfolio_percentages]
    
    # Determine the transaction fee, assuming no fee for cash
    transaction_fees = []
    for amount in invested_amounts[:-1]:  # Exclude cash for fee calculation
        if amount > 7334:
            fee = amount * 0.0009
        if amount == 0.0:
            fee = 0.0
        else:
            fee = 6.60
        transaction_fees.append(fee)
    transaction_fees.append(0)  # No fee for cash
    
    # Calculate net cash value after fees for all components including cash
    net_cash_values = [amount - fee for amount, fee in zip(invested_amounts, transaction_fees)]
    
    # Create a DataFrame to display the portfolio with cash values
    portfolio_df = pd.DataFrame({
        'Stock': portfolio_labels_d,
        'Invested Amount (AUD)': invested_amounts,
        'Transaction Fee (AUD)': transaction_fees,
        'Net Cash Value (AUD)': net_cash_values
    })
    # Calculate totals and sums for transactions
    total_sum_inv = portfolio_df['Invested Amount (AUD)'].sum()
    entry_sum_trans = portfolio_df['Transaction Fee (AUD)'].sum()
    entry_inv_from_trans = 0
    net_trans_cost = 0 + entry_sum_trans
    
    # Assign transaction cost summary
    # New row values
    new_row_values = ['trans_cost', entry_inv_from_trans, entry_sum_trans, net_trans_cost]
    
    # Adding new row using loc
    portfolio_df.loc[len(portfolio_df)] = new_row_values
    
    # Assign Start Date to each row
    portfolio_df['StartDate'] = start_date
    
    # Convert StartDate column to a list
    start_dates_list_d = portfolio_df['StartDate'].tolist()
    
    ############
    
    # Calculate the percentages for the legend
    portfolio_df['Percentage'] = (portfolio_df['Net Cash Value (AUD)'] / portfolio_df['Net Cash Value (AUD)'].sum()) * 100
    
    df_cash_start_d = portfolio_df.tail(2)
    cash_start_value_d = portfolio_df.loc[portfolio_df['Stock'] == 'Cash', 'Invested Amount (AUD)'].values[0]
    
    ##################
    
    # Getting the first column excluding the last two rows
    stock_names_d = portfolio_df.iloc[:-2, 0].tolist()
    stock_net_start_d = portfolio_df.iloc[:-2, 3].tolist()
    
    # Assuming df_close is already loaded and prepared
    investment_details = []
    
    # Iterate over stocks and their corresponding start dates
    for stock_symbol, start_date in zip(stock_names_d, start_dates_list_d):
        results = calculate_investment_details([start_date], stock_symbol, df_close)
        for start_price, latest_price in results:
            investment_details.append({
                "Stock": stock_symbol,
                "Price Bought": start_price,
                "Latest Price": latest_price
            })
    
    # Convert investment details to DataFrame
    investment_df_d = pd.DataFrame(investment_details)
    
    # Merging with the original portfolio DataFrame
    df_d = pd.merge(investment_df_d, portfolio_df, on='Stock', how='outer')
    df_d['hold_units_at_init'] = df_d['Net Cash Value (AUD)'] / df_d['Price Bought']
    
    
    ##### HIST 
    return hist_df_d,df_d,cash_start_value_d
    
##################
#########################
##################################

def _PORT_GRO_get():
    ### ##########################################################################
    ### Start Dates 
    len_stocks_g = len(portfolio_labels_g)
    start_date = ['2022-07-01'] * (len_stocks_g+2)
    
    ### Initial investments and portfolio setup
    portfolio_percentages = portfolio_percentages_g
        
    # data_to_append_df_g 
    ############################################################################
    #
    ############################################################################
    # history 
    df_columns = ['Stock', 'PercentSold', 'keep_drop', 'trans_type', 'DateTrans','exchange_stocks','sell_perc']
    hist_df_g = pd.DataFrame(columns=df_columns)  # Initialize with the updated columns
    
    # The data to append as a DataFrame, now excluding 'AmountSold' and 'AmountBought' # history of sells 
    hist_df_g = pd.concat([hist_df_g, data_to_append_df_g], ignore_index=True)
    
    # Ensure that all entries in 'exchange_stocks' and 'sell_perc' are lists of strings
    hist_df_g['exchange_stocks'] = hist_df_g['exchange_stocks'].apply(lambda lst: [str(item) for item in lst])
    hist_df_g['sell_perc'] = hist_df_g['sell_perc'].apply(lambda lst: [str(percentage) for percentage in lst])
    
    hist_df_g['id_time'] = hist_df_g['Stock'] + "_" + hist_df_g['DateTrans'] + "_" + hist_df_g['trans_type']
    
    # Save the DataFrame as a pickle file
    #hist_df_g.to_pickle('_1_tables/G_historic_data_.pkl')
    #print('History INIT wrote in pkl _1_tables/G_historic_data_.pkl \n')
    ############################################################################
    ############################################################################
    #######################################
    #
    initial_investment = initial_investment_G  # AUD
    #
    #print(f'\nInitial Investment is {initial_investment}')
    #
    # Calculate the total percentage currently allocated to stocks
    total_percentage_allocated = sum(portfolio_percentages)
    cash_percentage = 1 - total_percentage_allocated  # Remaining percentage for cash
    
    # Update the portfolio to include cash
    portfolio_percentages.append(cash_percentage)
    portfolio_labels_g.append('Cash')
    
    # Calculate invested amounts including the cash component
    invested_amounts = [percentage * initial_investment for percentage in portfolio_percentages]
    
    # Determine the transaction fee, assuming no fee for cash
    transaction_fees = []
    for amount in invested_amounts[:-1]:  # Exclude cash for fee calculation
        if amount > 7334:
            fee = amount * 0.0009
        if amount == 0.0:
            fee = 0.0
        else:
            fee = 6.60
        transaction_fees.append(fee)
    transaction_fees.append(0)  # No fee for cash
    
    # Calculate net cash value after fees for all components including cash
    net_cash_values = [amount - fee for amount, fee in zip(invested_amounts, transaction_fees)]
    
    # Create a DataFrame to display the portfolio with cash values
    portfolio_df = pd.DataFrame({
        'Stock': portfolio_labels_g,
        'Invested Amount (AUD)': invested_amounts,
        'Transaction Fee (AUD)': transaction_fees,
        'Net Cash Value (AUD)': net_cash_values
    })
    # Calculate totals and sums for transactions
    total_sum_inv = portfolio_df['Invested Amount (AUD)'].sum()
    entry_sum_trans = portfolio_df['Transaction Fee (AUD)'].sum()
    entry_inv_from_trans = 0
    net_trans_cost = 0 + entry_sum_trans
    
    # Assign transaction cost summary
    # New row values
    new_row_values = ['trans_cost', entry_inv_from_trans, entry_sum_trans, net_trans_cost]
    
    # Adding new row using loc
    portfolio_df.loc[len(portfolio_df)] = new_row_values
    
    # Assign Start Date to each row
    portfolio_df['StartDate'] = start_date
    
    # Convert StartDate column to a list
    start_dates_list_g = portfolio_df['StartDate'].tolist()
    
    ############
    
    # Calculate the percentages for the legend
    portfolio_df['Percentage'] = (portfolio_df['Net Cash Value (AUD)'] / portfolio_df['Net Cash Value (AUD)'].sum()) * 100
    
    df_cash_start_g = portfolio_df.tail(2)
    cash_start_value_g = portfolio_df.loc[portfolio_df['Stock'] == 'Cash', 'Invested Amount (AUD)'].values[0]
    
    ##################
    # Getting the first column excluding the last two rows
    stock_names_g = portfolio_df.iloc[:-2, 0].tolist()
    stock_net_start_g = portfolio_df.iloc[:-2, 3].tolist()
    
    # Creating a DataFrame to hold the investment details
    investment_details = []
    
    
    # Iterate over stocks and their corresponding start dates
    for stock_symbol, start_date in zip(stock_names_g, start_dates_list_g):
        results = calculate_investment_details([start_date], stock_symbol, df_close)
        for start_price, latest_price in results:
            investment_details.append({
                "Stock": stock_symbol,
                "Price Bought": start_price,
                "Latest Price": latest_price
            })
    # Convert investment details to DataFrame
    investment_df_g = pd.DataFrame(investment_details)
    
    # Merging with the original portfolio DataFrame
    df_g = pd.merge(investment_df_g, portfolio_df, on='Stock', how='outer')
    df_g['hold_units_at_init'] = df_g['Net Cash Value (AUD)'] / df_g['Price Bought']
    #
    #df_g.to_pickle('_1_tables/G_init_inv_.pkl')
    #print('\n\n INITIAL INV G_init_inv_.pkl has been written \n')
    return hist_df_g,df_g,cash_start_value_g

##############################################################################################
##############################################################################################
# _#_FN NAME ****** 9999 <<<      - sum units sold by stock -        >>> 9999 **********
############################ *********************************** #############################
######################################### - - - ##############################################
#END
import pandas as pd
from datetime import datetime, timedelta

def to_df_div(df):
    # Convert 'DateTrans' and 'StartDate' to datetime type, handling NaT properly
    df['DateTrans'] = pd.to_datetime(df['DateTrans'], errors='coerce')
    df['StartDate'] = pd.to_datetime(df['StartDate'], errors='coerce')
    
    # Identify duplicates based on 'Stock' and 'DateTrans'
    duplicates = df.duplicated(subset=['Stock', 'DateTrans'], keep=False)
    
    # Dataframe of duplicates
    df_duplicates = df[duplicates]
    
    # Aggregate the duplicates
    aggregated_duplicates = df_duplicates.groupby(['Stock', 'DateTrans']).agg({
        'units_updts': 'sum',     # Summing up 'units_updts'
        'StartDate': 'first',    # Keeping the first 'StartDate'
        'units_hold': 'first'    # Keeping the first 'units_hold'
    }).reset_index()
    
    # Dataframe of non-duplicates
    df_unique = df[~duplicates]
    
    df = pd.DataFrame()
    # Concatenate aggregated duplicates with non-duplicates
    df = pd.concat([df_unique, aggregated_duplicates], ignore_index=True)
    df = df.sort_values(by='Stock')
    
    ####################
    df_holds = df[df['units_hold'].notna()].copy() #df[df['units_hold'].isna()]
    #print('init_holds_ledger :\t ', len(df_holds))
    
    df_updts = df[df['units_hold'].isna()].copy()
    #print('update_ledger     :\t ',len(df_updts))
    
    # Convert date columns to datetime
    df_holds['StartDate'] = pd.to_datetime(df_holds['StartDate'])
    df_updts['DateTrans'] = pd.to_datetime(df_updts['DateTrans'])
    
    # Sorting
    df_updts = df_updts.sort_values(by=['Stock', 'DateTrans'])
    
    # Function to apply updates and expand DataFrame
    def update_holds(row):
        transactions = df_updts[df_updts['Stock'] == row['Stock']]
        results = []
        start_date = row['StartDate']
        units = row['units_hold']
        
        for _, trans in transactions.iterrows():
            end_date = trans['DateTrans']
            
            # Record period before transaction update
            results.append({'Stock': row['Stock'],
                            'StartDate': start_date,
                            'EndDate': end_date,
                            'units_hold': units})
            # Update units and set new start date for the next period
            units += trans['units_updts']
            start_date = end_date + timedelta(days=1)
        
        # Append the last period after the last transaction
        results.append({'Stock': row['Stock'], 
                        'StartDate': start_date,
                        'EndDate': pd.to_datetime(datetime.today().strftime('%Y-%m-%d')),
                        'units_hold': units})
        return results
    
    # Applying the updates and expanding DataFrame
    expanded_rows = df_holds.apply(update_holds, axis=1)
    df_div = pd.DataFrame([item for sublist in expanded_rows for item in sublist])
    
    # Check for negative units_hold and print a warning
    if (df_div['units_hold'] < 0).any():
        print("Warning: Negative stock holdings detected. Please check the transactions.")
    
    df_div['StartDate'] = df_div['StartDate'].dt.date
    df_div['EndDate'] = df_div['EndDate'].dt.date
    df_div['StartDate'] = pd.to_datetime(df_div['StartDate'])
    df_div['EndDate'] = pd.to_datetime(df_div['EndDate'])
    # SORT
    df_div = df_div.sort_values(by=['Stock', 'StartDate', 'EndDate'])
    df_div.to_pickle(f'_1_tables/_df_div_2_complete_LEDGER.pkl')
    return df_div
#######################################