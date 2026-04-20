##############################################################################################
################################IMPORTANT FUNCTIONS #######################################
import glob
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

def get_unique_stocks(portfolio_labels_g,portfolio_labels_d,stock_list_ce,df_add):
    stocks_add_unique = set(df_add['Stock'])
    unique_exchange_stocks = set(x for sublist in df_add['exchange_stocks'] for x in sublist)
    # Combine both sets to get all unique stocks
    all_unique_stocks = stocks_add_unique.union(unique_exchange_stocks)
    # Convert the set back to a list if needed
    all_unique_stocks_list_df_add = list(all_unique_stocks)
    
    # join all init 
    stock_list_all = portfolio_labels_g + portfolio_labels_d + stock_list_ce +all_unique_stocks_list_df_add 
    unique_stocks = list(set(stock_list_all))
    # GET rid of cash -> FOR UPDT stock list
    l_stocks_updt = [stock for stock in unique_stocks if stock not in ['CASH', 'Cash']]
    return l_stocks_updt
##################################################
##################################################
##################################################
################################################## GET FETCHED PRICES FROM table
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import numpy as np
import pandas as pd

def fetch_stock_price_on_date_close(stock, trans_date, df_close):
    """
    Fetches the closing price of a stock on a specific date from a pre-fetched DataFrame.
    If the date or stock symbol is not found or if the data is missing, checks up to three days prior in the same DataFrame.
    If still unavailable, prompts the user to input the missing price.
    """
    if stock == 'CASH':
        print('CASH detected -> ... Continuing')
        return 1

    try:
        date_obj = pd.to_datetime(trans_date, format='%Y-%m-%d')
    except ValueError:
        date_obj = pd.to_datetime(trans_date)

    if stock in df_close.columns:
        if date_obj in df_close.index and pd.notna(df_close.at[date_obj, stock]):
            return df_close.at[date_obj, stock]
        else:
            # Check up to three previous days if price is not available
            for days_back in range(1, 4):
                previous_date = date_obj - pd.Timedelta(days=days_back)
                if previous_date in df_close.index and pd.notna(df_close.at[previous_date, stock]):
                    print(f"Price not found on {date_obj.strftime('%Y-%m-%d')}, using {previous_date.strftime('%Y-%m-%d')} instead.\n")
                    return df_close.at[previous_date, stock]
    
    # If price is still not found, prompt user input
    print(f"Price data not found for {stock} on {trans_date} and three days prior.")
    new_price = float(input(f"Please enter the closing price for {stock} on {date_obj.strftime('%Y-%m-%d')}: "))
    df_close.at[date_obj, stock] = new_price  # Update the DataFrame with the new price
    df_close.to_pickle("_1_fetch/_0_fetched_stock_data_prices.pkl")  # Save the updated DataFrame
    return new_price
##################################################
##################################################
##################################################
################################################## CHECK & FETCH PRICES FROM YFINANCE


def fetch_stock_data(stock, start_date, end_date):
    stock_data = yf.download(stock, start=start_date, end=end_date)
    return stock_data['Close']

# Function to find the next available start date if data is missing
def find_valid_start_date(stock, start_date, current_date):
    while start_date <= current_date:
        data = fetch_stock_data(stock, start_date, start_date)
        if not data.empty:
            return start_date
        start_date += timedelta(days=1)
    return None

# Replace weekend prices with the previous Friday's price
def replace_weekend_with_friday(series):
    series = pd.to_numeric(series.replace('price_not_listed', np.nan), errors='coerce')
    for i in range(len(series)):
        if pd.isna(series[i]):
            # Check if the current day is Saturday or Sunday
            if series.index[i].weekday() == 5 or series.index[i].weekday() == 6:
                # Find the last Friday
                last_friday = series.index[i] - timedelta(days=series.index[i].weekday() - 4)
                if last_friday < series.index[0]:
                    continue  # Skip if the last Friday is before the series start
                series[i] = series.loc[last_friday]
            else:
                # If not a weekend, leave as NaN for now
                continue
    return series

# Main function to process stock data
def process_stock_data(stocks, start_date, end_date=datetime.now().strftime("%Y-%m-%d")):
    all_stocks_data = pd.DataFrame()

    for stock in stocks:
        data = fetch_stock_data(stock, start_date, end_date)

        if data.isnull().sum() > 14:
            next_valid_start = find_valid_start_date(stock, datetime.strptime(start_date, "%Y-%m-%d"), datetime.now())
            if next_valid_start:
                data = fetch_stock_data(stock, next_valid_start.strftime("%Y-%m-%d"), end_date)
                data = data.reindex(pd.date_range(start_date, end_date), fill_value='price_not_listed')
                data.loc[start_date:next_valid_start - timedelta(days=1)] = 'price_not_listed'
            else:
                data = pd.Series('price_not_listed', index=pd.date_range(start_date, end_date))
        else:
            data = data.reindex(pd.date_range(start_date, end_date), fill_value='price_not_listed')

        data.name = f'{stock}_Close'
        all_stocks_data = pd.concat([all_stocks_data, data], axis=1)

    all_stocks_data = all_stocks_data.apply(replace_weekend_with_friday)
    all_stocks_data.columns = [col.replace('_Close', '') for col in all_stocks_data.columns]

    all_stocks_data.to_pickle("_1_fetch/_0_fetched_stock_data_prices.pkl")  # Save DataFrame as pickle file
    return all_stocks_data

###
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

############################################# CHECK after fetching prices 
######################################## check days of the week missing data 
def check_nan_all():
    import pandas as pd
    
    def check_nan_frequency(file_path):
        # Load the DataFrame from a pickle file
        df = pd.read_pickle(file_path)
        
        # Prepare a dictionary to store the results
        nan_frequency = {}
        
        # Iterate over each column in the DataFrame
        for column in df.columns:
            # Drop non-NaN values and extract the weekday of NaN dates
            nan_days = df[column][df[column].isna()].index.weekday
            
            # Count the occurrences of each weekday
            counts = nan_days.value_counts().sort_index()
            
            # Map the weekday numbers to weekday names
            weekday_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
            counts.index = counts.index.map(weekday_names)
            
            # Store the result in the dictionary
            nan_frequency[column] = counts
        
        return nan_frequency
    
    # Example of how to use the function
    file_path = "_1_fetch/_0_fetched_stock_data_prices.pkl"
    nan_frequency = check_nan_frequency(file_path)
    for stock, freq in nan_frequency.items():
        print(f"NaN frequency for {stock}:\n{freq}\n")
    
######################################## check Max consecutive days missing 
    
    def max_consecutive_nans(file_path):
        # Load the DataFrame from a pickle file
        df = pd.read_pickle(file_path)
        
        # Prepare a dictionary to store the results
        max_nans = {}
        
        # Iterate over each column in the DataFrame
        for column in df.columns:
            # Convert the column to boolean where True indicates NaN
            is_nan = df[column].isna()
            
            # Calculate consecutive NaNs using a custom method
            # Using a cumulative sum of non-NaNs to define groups of consecutive NaNs
            if is_nan.any():  # Only process if there are any NaNs at all
                max_nans[column] = (is_nan.groupby((is_nan != is_nan.shift()).cumsum()).cumsum()).max()
            else:
                max_nans[column] = 0
        
        return max_nans
    
    # Mother function to orchestrate the reading and processing
    def analyze_stock_data(file_path):
        # Get maximum consecutive NaNs
        max_consecutive_nans_result = max_consecutive_nans(file_path)
        
        return max_consecutive_nans_result
    
    # Example of how to use the mother function
    file_path = "_1_fetch/_0_fetched_stock_data_prices.pkl"
    result = analyze_stock_data(file_path)
    for stock, max_nan in result.items():
        print(f"Maximum consecutive NaN days for {stock}: {max_nan}")

##################################################
##################################################
##################################################
################################################## GET FETCHED DIVIDENDS FROM table
#

def calculate_and_add_dividends(df):
    # Specify the path to your dividend data pickle file
    file_path = '_1_fetch/_1_fetched_stock_dividend_percentages.pkl'
    
    # Load the dividend data from the pickle file
    dividend_data = pd.read_pickle(file_path)

    def get_dividends(row):
        # Filter the dividend data for the specified stock and within the date range
        applicable_dividends = dividend_data[
            (dividend_data.index >= row['StartDate']) & 
            (dividend_data.index <= row['AnalysisEndDate'])
        ].get(row['Stock'], pd.Series(dtype='float64')).sum()
        return applicable_dividends

    # Check if 'units_hold' column exists, if not add it and set to 1
    if 'units_hold' not in df.columns:
        df['units_hold'] = 1  # Default to 1 if not present
        print("\n*ATTN*\n**\n* No 'units_hold' column found, setting all units to 1.")

    # Calculate dividends for each row and apply units_hold factor
    df['Dividends'] = df.apply(get_dividends, axis=1) * df['units_hold']

    return df;

##################################################
##################################################
##################################################
################################################## CHECK & FETCH DIVIDENDS FROM YFINANCE

# Initialize a cache for dividends to avoid redundant network calls
dividend_cache = {}

def get_cached_dividends(stock):
    if stock not in dividend_cache:
        ticker = yf.Ticker(stock)
        dividends = ticker.dividends
        dividends.index = dividends.index.tz_localize(None)  # Ensure timezone-naive
        dividend_cache[stock] = dividends
    return dividend_cache[stock]

def add_custom_dividends(stock, start_date, end_date, frequency='M', dividend_amount=0.155):
    if stock == 'TACT.XA':  # Example to add manual dividends for a specific stock
        dates = pd.date_range(start=start_date, end=end_date, freq=frequency) + pd.tseries.offsets.MonthEnd(0)
        dividends = pd.Series(dividend_amount, index=dates)
        return dividends
    return pd.Series([])  # Return an empty series for other stocks

def fetch_dividend_analysis(l_stocks_updt, start_date, end_date=None, custom_dividends=True):
    # Setting up end date
    end_date = end_date or pd.Timestamp.today().normalize()
    
    # Create a dictionary to hold dividend data
    dividend_data = {}
    
    # Fetch or generate dividend data for each stock
    for stock in l_stocks_updt:
        if custom_dividends and stock == 'TACT.XA':
            dividend_data[stock] = add_custom_dividends(stock, start_date, end_date)
        else:
            dividend_data[stock] = get_cached_dividends(stock)[start_date:end_date]
    
    # Convert dictionary into DataFrame
    df_dividends = pd.DataFrame(dividend_data)
    
    # Fill missing dates with 0
    df_dividends.fillna(0, inplace=True)
    
    # Save the DataFrame to a pickle file
    file_path = '_1_fetch/_1_fetched_stock_dividend_percentages.pkl'
    df_dividends.to_pickle(file_path)
    print(f"Table has been written as '{file_path}'")

#
##############################################################################################
##############################################################################################
############################################################################################## 
##############################################################################################
# _#_FN NAME ****** 9999 <<<      - sum units sold by stock -        >>> 9999 **********
############################ *********************************** #############################
######################################### - - - ##############################################
#
#

import pandas as pd

def fill_missing_values(file_path):
    # Load the DataFrame from a pickle file
    df = pd.read_pickle(file_path)
    
    # Analyze and fill NaNs based on the specified conditions
    for column in df.columns:
        # Identify where NaNs are located
        is_nan = df[column].isna()
        
        # Calculate the number of consecutive NaNs
        consec_nans = is_nan.groupby((is_nan != is_nan.shift()).cumsum()).cumsum()
        
        # Determine where consecutive NaNs are less than 7 days
        valid_fill_indices = consec_nans[(consec_nans < 7) & (is_nan)].index
        
        # Iterate through valid NaN indices to fill them
        for idx in valid_fill_indices:
            # Look back up to 8 days to find a non-NaN value to fill
            for look_back in range(1, 9):  # Check up to 8 days back
                if idx - pd.Timedelta(days=look_back) in df.index:
                    fill_value = df[column].loc[idx - pd.Timedelta(days=look_back)]
                    if pd.notna(fill_value):
                        df.at[idx, column] = fill_value
                        break  # Stop after finding the first non-NaN value
                
    return df

from datetime import datetime, timedelta
########### important one
def main_stock_table_fetched(l_stocks_updt,d_start_date):
    stocks = l_stocks_updt 
    start_date = d_start_date  
    end_date = datetime.now().strftime("%Y-%m-%d") 
    # run main fn  to fetch 
    df_close = process_stock_data(stocks, start_date)
    # fix main table fetched 
    file_path = "_1_fetch/_0_fetched_stock_data_prices.pkl"
    df_filled = fill_missing_values(file_path)
    df_filled.to_pickle(f"{file_path}")
    rsp = input('Do you want to CHECK nan ?\n')
    if rsp == 'y':
        check_nan_all()
        print('Table Written')
    return

# def main_stock_table_fetched(new_stocks,d_start_date):
#     stocks = l_stocks_updt 
#     start_date = d_start_date  
#     end_date = datetime.now().strftime("%Y-%m-%d") 
#     # run main fn  to fetch 
#     df_close_new = process_stock_data(stocks, start_date)
#     # fix main table fetched 
#     file_path = "_1_fetch/_0_fetched_stock_data_prices_new_stocks.pkl"
#     df_filled = fill_missing_values(file_path)
#     df_filled.to_pickle("_1_fetch/_0_fetched_stock_data_prices.pkl")
#     rsp = input('Do you want to CHECK nan ?\n')
#     if rsp == 'y':
#         check_nan_all()
#         print('Table Written')
#     return
# #
#
##############################################################################################
##############################################################################################
############################################################################################## 
##############################################################################################
# _#_FN NAME ****** 9999 <<<      - sum units sold by stock -        >>> 9999 **********
############################ *********************************** #############################
######################################### - - - ##############################################
#
#
import pandas as pd

def sum_units_sold_by_stock_bought(df, stock_names):
    import datetime
    from datetime import datetime
    results = []

    for stock_name in stock_names:
        stock_df = df[df['Stock'] == stock_name].copy()
        
        # Ensure units_acquired is in float for accurate rounding
        stock_df['units_acquired'] = stock_df['units_acquired'].astype(float)
        
        # Round the units_acquired values to two decimals and convert them to strings
        units_acquired_list = [f"{value:.2f}" for value in stock_df['units_acquired']]
        
        # Join the rounded, string-converted values with ' + '
        operation_str = ' + '.join(units_acquired_list)
        
        # Sum the rounded units_acquired for the current stock
        total_units = round(stock_df['units_acquired'].sum(), 2)
        
        results.append((stock_name, total_units, operation_str))

    results_df = pd.DataFrame(results, columns=['Stock', 'Total Units Bought', 'Operation'])
    return results_df
#
#
##############################################################################################
##############################################################################################
############################################################################################## 
##############################################################################################
# _#_FN NAME ****** 9999 <<<      - sum units sold by stock -        >>> 9999 **********
############################ *********************************** #############################
######################################### - - - ##############################################
#
#
def sum_units_sold_by_stock_sold(df, stock_names):

    results = []

    for stock_name in stock_names:
        # Filter the DataFrame for the current stock and explicitly create a copy to avoid the SettingWithCopyWarning
        stock_df = df[df['Stock'] == stock_name].copy()
        
        # Ensure units_sold is in float for accurate rounding, then round the values and convert them to strings
        units_sold_list = [f"{value:.2f}" for value in stock_df['units_sold']]
        
        # Create a string that depicts the rounded addition of units_sold for the stock
        operation_str = ' + '.join(units_sold_list)
        
        # Sum the 'units_sold' for the current stock, rounding the total to maintain consistency
        total_units = round(stock_df['units_sold'].sum(), 2)
        
        # Append the result as a tuple (stock name, total units sold, operation string)
        results.append((stock_name, total_units, operation_str))

    # Convert the results list of tuples into a DataFrame for a tabular presentation
    results_df = pd.DataFrame(results, columns=['Stock', 'Total Units Sold', 'Operation'])
    return results_df
#
#
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
# _#_FN NAME ****** 9999 <<<      - sum units sold by stock -        >>> 9999 **********
############################ *********************************** #############################
######################################### - - - ##############################################
#
#

def sum_buy_sell_ordered(df_all_buy, df_all_sell):
    # Initialize a list to hold the results
    results = []
    
    # Assume both DataFrames have the same length and stock order
    for i in range(len(df_all_buy)):
        # Access each row by index
        buy_row = df_all_buy.iloc[i]
        sell_row = df_all_sell.iloc[i]
        
        # Check if the stocks are the same in both rows
        if buy_row['Stock'] == sell_row['Stock']:
            stock_name = buy_row['Stock']
            total_units_bought = round(buy_row['Total Units Bought'], 2)
            total_units_sold = round(sell_row['Total Units Sold'], 2)
            
            # Use the operation strings directly from the rows
            operation_buy_str = buy_row['Operation']
            operation_sell_str = sell_row['Operation']
            
            # Append the result
            results.append((stock_name, total_units_bought, operation_buy_str, total_units_sold, operation_sell_str))
        else:
            print(f"Stock mismatch at row {i}: {buy_row['Stock']} vs {sell_row['Stock']}")
            # Handle the mismatch case as needed

    # Convert the results list of tuples into a DataFrame
    results_df = pd.DataFrame(results, columns=['Stock', 'Total Units Bought', 'Buy Operation', 'Total Units Sold', 'Sell Operation'])

    return results_df

############################

import pandas as pd
from datetime import datetime

def analyze_dates(df, count_back_from_date):
    # Ensure count_back_from_date is a datetime object
    if isinstance(count_back_from_date, str):
        count_back_date = datetime.strptime(count_back_from_date, '%Y-%m-%d')
    else:
        count_back_date = count_back_from_date
    
    # Define a function to determine the appropriate 'AnalysisEndDate'
    def determine_analysis_end(row, count_back_date):
        start_date = row['StartDate']
        end_date = row['EndDate']
        
        # Check if EndDate is less than StartDate
        if end_date < start_date:
            error_msg = f"Error: EndDate {end_date} is before StartDate {start_date} for Stock {row['Stock']}"
            print(error_msg)
            return "Error: Invalid date range"

        # Determine AnalysisEndDate based on date comparisons
        if start_date > count_back_date:
            return 'start date greater than count_back_from_date'
        elif end_date < count_back_date:
            return end_date.strftime('%Y-%m-%d')
        else:
            return count_back_date.strftime('%Y-%m-%d')
    
    # Apply the function to each row
    df['AnalysisEndDate'] = df.apply(determine_analysis_end, args=(count_back_date,), axis=1)
    
    # Add 'run_date' and 'count_back_from_date' columns to the DataFrame
    today_date = datetime.now().strftime('%Y-%m-%d')
    df['run_date'] = today_date
    df['count_back_from_date'] = count_back_date

    # Sub-function to handle rows to potentially delete
    handle_deletion(df)

    return df

def handle_deletion(df):
    # Filter rows where AnalysisEndDate indicates a greater start date
    deletion_candidates = df[df['AnalysisEndDate'] == 'start date greater than count_back_from_date']
    
    if not deletion_candidates.empty:
        print("These rows have a start date greater than count_back_from_date:")
        print(deletion_candidates)
        
        # Ask user if they want to delete these rows
        response = input("Do you want to delete all of these rows? (yes/no) ")
        if response.lower() == 'yes':
            # Remove the rows from the DataFrame
            df.drop(deletion_candidates.index, inplace=True)
            print("Rows deleted.")
        else:
            print(" no action !! ")
    else:
        print("- - - - - - - - - - - - - > LEDGER PROCESSED")


### follow up 
def filter_df_by_months_and_analysis_dates_and_DIVS(df, months_ago, date_column,cutoff_date_custom):
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
    today = pd.to_datetime(cutoff_date_custom) ################# custom DATE
    cutoff_date = today - pd.DateOffset(months=months_ago)

    # Filter the DataFrame accordingly
    if months_ago == 0:
        filtered_df = df.copy()
    else:
        filtered_df = df[df[date_column] < cutoff_date].copy()  # Explicit copy to avoid SettingWithCopyWarning

    # Add new columns
    #filtered_df['run_date'] = today.strftime('%Y-%m-%d')  # The date when the function is run
    #filtered_df['count_back_from_date'] = (today - pd.DateOffset(months=months_ago)).strftime('%Y-%m-%d') 
    cutoff_date = (today - pd.DateOffset(months=months_ago)).strftime('%Y-%m-%d')
    print(cutoff_date)
    # The start date from which the algorithm counts back
    filtered_df = analyze_dates(filtered_df, cutoff_date)

    # COMPUTE DIVIDENDS
    filtered_df  = calculate_and_add_dividends(filtered_df )

    
    return filtered_df
        
 #
#
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
# _#_FN NAME ****** 9999 <<<      - sum units sold by stock -        >>> 9999 **********
############################ *********************************** #############################
######################################### - - - ##############################################
#
#

