################################################################
import pandas as pd
from datetime import datetime
from _fns import fetch_stock_price_on_date_close
################################################################

################################################################
df_div = pd.read_pickle(f'_1_tables/_df_div_11_breakdown_LEDGER.pkl')

df_div['EndDate'] = pd.to_datetime(df_div['EndDate'])
df_div = df_div[df_div['units_hold'] != 0.0]

################################################################
df_close = pd.read_pickle("_1_fetch/_0_fetched_stock_data_prices.pkl")
# Ensure that the index is of datetime type if it isn't already
if not pd.api.types.is_datetime64_any_dtype(df_close.index):
    df_close.index = pd.to_datetime(df_close.index)

#df_close.tail(97)
# #fetch_stock_price_on_date_close(stock, trans_date, df_close):
################################################################

################################################################


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
###############################################################
###############################################################
###############################################################
# MONTHLY 
_df_0m = filter_df_by_months(df_div,0, 'StartDate')
_df_1m = filter_df_by_months(df_div,1, 'StartDate')
_df_2m = filter_df_by_months(df_div,2, 'StartDate')
_df_3m = filter_df_by_months(df_div,3, 'StartDate')
_df_4m = filter_df_by_months(df_div,4, 'StartDate')
_df_5m = filter_df_by_months(df_div,5, 'StartDate')
_df_6m = filter_df_by_months(df_div,6, 'StartDate')
_df_7m = filter_df_by_months(df_div,7, 'StartDate')
_df_8m = filter_df_by_months(df_div,8, 'StartDate')
_df_9m = filter_df_by_months(df_div,9, 'StartDate')
_df_10m = filter_df_by_months(df_div,10, 'StartDate')
_df_11m = filter_df_by_months(df_div,11, 'StartDate')
_df_12m = filter_df_by_months(df_div,12, 'StartDate')
_df_13m = filter_df_by_months(df_div,13, 'StartDate')
_df_14m = filter_df_by_months(df_div,14, 'StartDate')
_df_15m = filter_df_by_months(df_div,15, 'StartDate')
_df_16m = filter_df_by_months(df_div,16, 'StartDate')

_df_17m = filter_df_by_months(df_div,17, 'StartDate')
_df_18m = filter_df_by_months(df_div,18, 'StartDate')
_df_19m = filter_df_by_months(df_div,19, 'StartDate')

_df_20m = filter_df_by_months(df_div,20, 'StartDate')

_df_21m = filter_df_by_months(df_div,21, 'StartDate')


range_concat = 21
############### ADD NEXT 5 MONTHS TO CUE
from datetime import datetime

# APRIL
if (datetime.now() - datetime(datetime.now().year, 4, 1)).days >= 30:
    _df_22m = filter_df_by_months(df_div,22, 'StartDate');print('ap')
    range_concat = range_concat + 1

# MAY
if (datetime.now() - datetime(datetime.now().year, 5, 1)).days >= 30:
    _df_23m = filter_df_by_months(df_div,23, 'StartDate');print('may')
    range_concat = range_concat + 1

# JUNE
if (datetime.now() - datetime(datetime.now().year, 6, 1)).days >= 30:
    _df_24m = filter_df_by_months(df_div,24, 'StartDate');print('jun')
    range_concat = range_concat + 1

    
# JULY
if (datetime.now() - datetime(datetime.now().year, 7, 1)).days >= 30:
    _df_25m = filter_df_by_months(df_div,25, 'StartDate');print('jul')
    range_concat = range_concat + 1

    
# AUGUST
if (datetime.now() - datetime(datetime.now().year, 8, 1)).days >= 30:
    _df_26m = filter_df_by_months(df_div,26, 'StartDate');print('aug')
    range_concat = range_concat + 1


###############################################################
###############################################################
###############################################################

import pandas as pd

# Assuming the function filter_df_by_months and DataFrame df_div are defined

# Generate a list of filtered DataFrames using a list comprehension
dfs = [filter_df_by_months(df_div, month, 'StartDate') for month in range(range_concat+1)]

# Concatenate all the filtered DataFrames into a single DataFrame
df_all = pd.concat(dfs, ignore_index=True)


###############################################################
###############################################################
###############################################################

import pandas as pd

def categorize_dates(df, date_column):
    # Ensure run_date is in datetime format
    df[date_column] = pd.to_datetime(df[date_column])

    # Sort DataFrame by date
    df_sorted = df.sort_values(by=date_column, ascending=False)

    # Rank dates and create a category
    df_sorted['date_category'] = (df_sorted[date_column]
                                  .rank(method='dense', 
        ascending=False) - 1).astype(int).astype(str) + 'm'

    return df_sorted

# Assume df_all is your DataFrame and 'run_date' is your date column
df_all = categorize_dates(df_all, 'count_back_from_date')



###############################################################


import yfinance as yf
from datetime import datetime
import pandas as pd

# Assuming df_all is your dataframe and it's already defined
# Add a column to df_all for the closing prices
df_all['closing_price'] = None

for index, row in df_all.iterrows():
    closing_price = fetch_stock_price_on_date_close(row['Stock'], row['count_back_from_date'],df_close)
    df_all.at[index, 'closing_price'] = closing_price



#Assuming df_all is your dataframe and it already has a 'closing_price' column

# Count the number of entries with no value (None)
none_count = df_all['closing_price'].isna().sum()

# Count the number of entries with a value of 0
zero_count = (df_all['closing_price'] == 0).sum()

# Count the number of entries with a non-zero value
value_count = df_all['closing_price'].notna().sum() - zero_count

print(f"Number of entries with no value (None): {none_count}")
print(f"Number of entries with a value of 0: {zero_count}")
print(f"Number of entries with a non-zero value: {value_count}")
df_all['holding_value'] = df_all['units_hold'] * df_all['closing_price']


####################################################
import pandas as pd

# Assuming df_all is your DataFrame
# Convert EndDate to datetime if it's not already
df_all['EndDate'] = pd.to_datetime(df_all['EndDate'])

# Initialize an empty DataFrame to hold the filtered results
filtered_df = pd.DataFrame()

# Group the DataFrame by 'date_category'
grouped = df_all.groupby('date_category')

# For each 'date_category', sort by 'Stock' and 'EndDate', then drop duplicates
for _, group in grouped:
    sorted_group = group.sort_values(by=['Stock', 'EndDate'])
    unique_latest = sorted_group.drop_duplicates(subset='Stock', keep='last')
    # Append the filtered group to the filtered_df DataFrame
    filtered_df = pd.concat([filtered_df, unique_latest], ignore_index=True)

    
#filtered_df now contains only the most recent entry for each stock within each date_category

# Convert 'count_back_from_date' to datetime if it's not already
filtered_df['count_back_from_date'] = pd.to_datetime(filtered_df['count_back_from_date'])

# Group by 'date_category', sum 'holding_value', and keep the first 'count_back_from_date'
grouped_df = filtered_df.groupby('date_category').agg(
    total_holding_value=('holding_value', 'sum'),
    count_back_from_date=('count_back_from_date', 'first')  # Assumes this makes sense for your data
)

# Reset the index to turn 'date_category' back into a column
grouped_df = grouped_df.reset_index()

# Sort by 'count_back_from_date'
df_mos = grouped_df.sort_values(by='count_back_from_date')

df_mos


from datetime import datetime

def convert_dates(dates):
    """
    Converts a list of dates into a specific string format "Mon day year'".
    Only the first three letters of the month are included.
    
    Parameters:
    - dates: List of dates, can be strings or datetime objects.
    
    Returns:
    - A list of strings, where each date is formatted as "Mon day year'".
    """
    formatted_dates = []
    for date in dates:
        # Ensure each date is a datetime object
        if isinstance(date, str):
            # Adjust the format '%Y-%m-%d' as per your input date format
            date_obj = datetime.strptime(date, '%Y-%m-%d')
        elif isinstance(date, datetime):
            date_obj = date
        else:
            raise ValueError("Date format not recognized. Must be string or datetime.datetime object.")
        
        # Convert the datetime object to the specified format "Mon day year'"
        # Using '%b' for abbreviated month name, '%d' for day of the month, and '%y' for two-digit year
        formatted_date = date_obj.strftime('%b %d %y\'')
        formatted_dates.append(formatted_date.strip())
    
    return formatted_dates


# Example usage:
# Assuming `actual_months` is your list of dates from the DataFrame column
actual_months = df_mos['count_back_from_date'].tolist()
df_mos['dates'] = convert_dates(actual_months)
# print(formatted_dates)




import pandas as pd

# Ensure the data is sorted by date_category and round the total_holding_value
df_mos['total_holding_value'] = df_mos['total_holding_value'].round(2)
#df_mos.sort_values(by='date_category', inplace=True)

# Adjusted graph function to work with DataFrame
def ascii_graph_from_df(df):
    months = df['date_category'].tolist()
    actual_months = df['dates'].tolist()

    amounts = df['total_holding_value'].tolist()
    max_amount = max(amounts)
    graph_lines = []
    prev_amount = None

    for month, amount ,actual_months in zip(months, amounts,actual_months):
        bar_chars = int((amount / max_amount) * 40)  # Scale to graph width of 50
        color_code = "\033[92m" if prev_amount is None or amount >= prev_amount else "\033[91m"
        graph_line = f"\t* {actual_months} \t{''}{color_code}{amount}\033[0m  \t{'█' * bar_chars}  *** {month}"
        graph_lines.append(graph_line)
        prev_amount = amount

    return '\n'.join(graph_lines)

# Generate and print the ASCII graph from the DataFrame
ascii_graph_output = ascii_graph_from_df(df_mos)



print('************************************************************************************************')
print('************************************************************************************************')
print('************************************************************************************************\n')

print(ascii_graph_output)  # This will not show colors here, run it in your terminal for colored output

print('\n************************************************************************************************')
print('************************************************************************************************')
print('************************************************************************************************')












