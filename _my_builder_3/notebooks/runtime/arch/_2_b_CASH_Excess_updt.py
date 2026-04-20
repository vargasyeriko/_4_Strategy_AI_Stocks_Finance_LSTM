
    
################################################################

################################################################

################################################################

################################################################

################################################################

################################################################
import pandas as pd
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

# Example usage
_df_0m = filter_df_by_months(df_div,0, 'StartDate')
_df_3m = filter_df_by_months(df_div,3, 'StartDate')
_df_6m = filter_df_by_months(df_div,6, 'StartDate')
_df_12m = filter_df_by_months(df_div,12, 'StartDate') # CHANGE to 12 months 
 ################################################################
################################################################
import pandas as pd

# Define the function to compare and create 'AnalysisEndDate'
def compare_and_set_analysis_end_date(df):
    # Ensure both columns are in datetime format
    df['EndDate'] = pd.to_datetime(df['EndDate'])
    df['count_back_from_date'] = pd.to_datetime(df['count_back_from_date'])
    
    # Adjust the condition as per the new requirement
    df['AnalysisEndDate'] = df.apply(lambda row: row['count_back_from_date'] if row['count_back_from_date'] < row['EndDate'] else row['EndDate'], axis=1)
    return df

# Assuming _df_0m, _df_3m, _df_6m, _df_9m are your DataFrames and they're already defined
# List of DataFrames for iteration
dfs = [_df_0m, _df_3m, _df_6m, _df_12m]

# Apply the function to each DataFrame
dfs = [compare_and_set_analysis_end_date(df) for df in dfs]

# Now, dfs contains the modified DataFrames with the correct 'AnalysisE

################################################################
################################################################

# ADD DIVIDENDS
import pandas as pd
import yfinance as yf

# Assuming _df_0m, _df_3m, _df_6m, _df_9m are already defined DataFrames

# Initialize a cache for dividends to minimize API calls
dividend_cache = {}

# Function to fetch and cache dividends
def get_cached_dividends(stock):
    if stock not in dividend_cache:
        ticker = yf.Ticker(stock)
        dividends = ticker.dividends
        dividends.index = dividends.index.tz_localize(None)  # Ensure timezone-naive
        dividend_cache[stock] = dividends
    return dividend_cache[stock]

# Function to calculate dividends for a DataFrame
def calculate_and_add_dividends(df):
    # Ensure 'StartDate' and 'AnalysisEndDate' are datetime
    df['StartDate'] = pd.to_datetime(df['StartDate'])
    df['AnalysisEndDate'] = pd.to_datetime(df['AnalysisEndDate'])
    
    # Calculate dividends
    def get_dividends(row):
        dividends = get_cached_dividends(row['Stock'])
        relevant_dividends = dividends[(dividends.index >= row['StartDate']) & (dividends.index <= row['AnalysisEndDate'])]
        return relevant_dividends.sum()

    # Assuming 'units_hold' column exists or setting it to 1 for calculation
    df['Dividends'] = df.apply(get_dividends, axis=1) * df['units_hold']
    return df

# Apply the function to each DataFrame
_df_0m = calculate_and_add_dividends(_df_0m)
_df_3m = calculate_and_add_dividends(_df_3m)
_df_6m = calculate_and_add_dividends(_df_6m)
_df_12m = calculate_and_add_dividends(_df_12m)

# # At this point, each DataFrame (_df_0m, _df_3m, _df_6m, _df_9m) has a new column 'Dividends'

# # start to 12 month ago we received n dividens -> flip it to know from now to back 12 months

# # start to 9 month ago we received n dividens 

# # start to 6 month ago we received n dividens 

# last_6m_div = 531.653298 -360.152234
# last_6m_div
# # start to 3 month ago we received n dividens ##################################################################### 

# want to run this 6-8 of the month 

# 3 months -> change the end date for March 8 
################################################################
################################################################

# ADD DIV value  SUm
_df_0m_info = _df_0m.groupby('Stock')['Dividends'].sum().reset_index().rename(columns={'Dividends': 'dividend_total'})
_df_0m = _df_0m.merge(_df_0m_info, on='Stock').copy()


# Sort by 'Stock' and 'AnalysisEndDate' in descending order
_df_0m = _df_0m.sort_values(by=['Stock', 'AnalysisEndDate'], ascending=[True, False])

# Drop duplicates based on 'Stock', keeping the first (most recent 'AnalysisEndDate')
_df_0m = _df_0m.drop_duplicates(subset='Stock', keep='first')

_df_0m['m_period']  = '0m'



################################################################
################################################################


# ADD DIV value  SUm
_df_3m_info = _df_3m.groupby('Stock')['Dividends'].sum().reset_index().rename(columns={'Dividends': 'dividend_total'})
_df_3m = _df_3m.merge(_df_3m_info, on='Stock').copy()


# Sort by 'Stock' and 'AnalysisEndDate' in descending order
_df_3m = _df_3m.sort_values(by=['Stock', 'AnalysisEndDate'], ascending=[True, False])

# Drop duplicates based on 'Stock', keeping the first (most recent 'AnalysisEndDate')
_df_3m = _df_3m.drop_duplicates(subset='Stock', keep='first')

_df_3m['m_period']  = '3m'
################################################################
################################################################


# ADD DIV value  SUm
_df_6m_info = _df_6m.groupby('Stock')['Dividends'].sum().reset_index().rename(columns={'Dividends': 'dividend_total'})
_df_6m = _df_6m.merge(_df_6m_info, on='Stock').copy()


# Sort by 'Stock' and 'AnalysisEndDate' in descending order
_df_6m = _df_6m.sort_values(by=['Stock', 'AnalysisEndDate'], ascending=[True, False])

# Drop duplicates based on 'Stock', keeping the first (most recent 'AnalysisEndDate')
_df_6m = _df_6m.drop_duplicates(subset='Stock', keep='first')

_df_6m['m_period'] = '6m'
################################################################
################################################################


# ADD DIV value  SUm
_df_12m_info = _df_12m.groupby('Stock')['Dividends'].sum().reset_index().rename(columns={'Dividends': 'dividend_total'})
_df_12m = _df_12m.merge(_df_12m_info, on='Stock').copy()


# Sort by 'Stock' and 'AnalysisEndDate' in descending order
_df_12m = _df_12m.sort_values(by=['Stock', 'AnalysisEndDate'], ascending=[True, False])

# Drop duplicates based on 'Stock', keeping the first (most recent 'AnalysisEndDate')
_df_12m = _df_12m.drop_duplicates(subset='Stock', keep='first')


_df_12m['m_period'] = '12m'

################################################################

div_total_0 =_df_0m['dividend_total'].sum()

div_total_3 =_df_3m['dividend_total'].sum()

div_total_6 =_df_6m['dividend_total'].sum()

div_total_12 =_df_12m['dividend_total'].sum()

print('\n\n ATTN ::: div_total 0,3,6,12 months resp:::\n',div_total_0,div_total_3,div_total_6,div_total_12,'\n\n',)


################################################################
################################################################
# BUILD MASTER TABLE
################################################################
################################################################
import pandas as pd

def concat_dfs(dfs, columns_to_keep=[]):
   
    # Check if specific columns are provided for the final dataframe
    if columns_to_keep:
        # Filter each dataframe to keep only the specified columns (if they exist in that dataframe)
        filtered_dfs = [df[columns_to_keep] for df in dfs if set(columns_to_keep).issubset(df.columns)]
    else:
        # If no columns are specified, use all dataframes as they are
        filtered_dfs = dfs
    
    # Concatenate all the filtered dataframes
    final_df = pd.concat(filtered_dfs, ignore_index=True)
    
    return final_df

# Example usage:
# df1 = pd.DataFrame(...)
# df2 = pd.DataFrame(...)
# df3 = pd.DataFrame(...)
# df4 = pd.DataFrame(...)
dfs = [_df_0m,_df_3m ,_df_6m,_df_12m]
columns_to_keep = ['Stock','units_hold','m_period', 'dividend_total','AnalysisEndDate']
df_master = concat_dfs(dfs, columns_to_keep)

################################################################

###################### export ABOVE for _df_0m_ ==== > needs work entry updt program is failing

# _df_0m.to_pickle(f'_1_tables/_2_up_to_date_df0m_.pkl')
# print(len(_df_0m),'\n Exporting updt DF for future buys/sells ::_2_up_to_date_df0m_.pkl::\n','\n')

# ###################### export ABOVE for div master_df for returns and graphs etc 

    



# ###################### and last one this one is for Cash stuff 

# # Assuming 'cash_start_value_d' is a variable holding the value you want to assign

# # Add a new column 'cash_start_d' and initialize with NaN or some default value for all rows
# df_cash_bal['cash_start_d'] = None  # or use np.nan if you prefer to initialize with NaN
# df_cash_bal['cash_start_g'] = None  # or use np.nan if you prefer to initialize with NaN


# # Now, update this new column's value based on the condition that 'trans_type' equals 'cash_init'
# df_cash_bal.loc[df_cash_bal['trans_type'] == 'cash_init', 'cash_start_d'] = cash_start_value_d
# df_cash_bal.loc[df_cash_bal['trans_type'] == 'cash_init', 'cash_start_g'] = cash_start_value_g

# # df_cash_bal now has the new column 'cash_start_d' with the specified value where 'trans_type' is 'cash_init'

# df_cash_bal.to_pickle(f'_1_tables/_3_up_to_date_cash_bal_.pkl')
# print(len(_df_0m),'\n Exporting updt DF for future buys/sells ::_2_up_to_date_df0m_.pkl::\n','\n')

# # EXPORT DIVIDENDS NOW 4 

    
# df_master.to_pickle(f'_1_tables/_4_up_to_date_dividends.pkl');print('df_master exported to ::: _4_up_to_date_dividends.pkl')
# # #_2_## GRAPHS


