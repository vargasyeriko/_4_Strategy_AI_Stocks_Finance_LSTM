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

#input('_1_a_Cash')




#import pandas as pd
# Convert all dates to datetime, sort by 'Stock', and then by 'StartDate' or 'DateTrans'
df['StartDate'] = pd.to_datetime(df['StartDate'], errors='coerce')
df['DateTrans'] = pd.to_datetime(df['DateTrans'], errors='coerce')
df.sort_values(by=['Stock', 'StartDate', 'DateTrans'], inplace=True)

# Replace NaN in 'units_updts' with 0 for cumulative calculation
df['units_updts'].fillna(0, inplace=True)

import pandas as pd
from datetime import datetime

def calculate_holding_periods_(group):
    records = []
    current_units = 0
    start_date = None

    # Iterate over the rows in the group
    for index, row in group.iterrows():
        # Check if it's the start of a new holding period
        if not pd.isna(row['StartDate']) and not pd.isna(row['units_hold']):
            # If current_units are not zero, record the previous period
            if current_units != 0:
                records += [{
                    'Stock': row['Stock'],
                    'StartDate': start_date,
                    'EndDate': row['StartDate'] - pd.Timedelta(days=1),
                    'units_hold': current_units
                }]
            # Reset for the new holding period
            current_units = row['units_hold']
            start_date = row['StartDate']
        
        # Check if there's a transaction update
        if not pd.isna(row['DateTrans']):
            records += [{
                'Stock': row['Stock'],
                'StartDate': start_date,
                'EndDate': row['DateTrans'],
                'units_hold': current_units
            }]
            # Update the units and move the start date forward
            current_units += row['units_updts']
            start_date = row['DateTrans'] + pd.Timedelta(days=1)

    # Append the final period that extends to the current day
    records += [{
        'Stock': group.iloc[-1]['Stock'],
        'StartDate': start_date,
        'EndDate': datetime.now(),
        'units_hold': current_units
    }]

    # Convert the list of dictionaries to a DataFrame at the end
    return pd.DataFrame(records)

# Assuming 'df' is your DataFrame
# Group by 'Stock' and apply the function
holding_periods = df.groupby('Stock').apply(calculate_holding_periods_).reset_index(drop=True)

# Convert the holding periods to a DataFrame
df_holding_periods = pd.DataFrame(holding_periods)
df_div = df_holding_periods.explode('Stock').reset_index(drop=True)





# Convert 'StartDate' and 'EndDate' to just date (without time)
df_div['StartDate'] = df_div['StartDate'].dt.date
df_div['EndDate'] = df_div['EndDate'].dt.date
df_div['StartDate'] = pd.to_datetime(df_div['StartDate'])
df_div['EndDate'] = pd.to_datetime(df_div['EndDate'])
# SORT
df_div = df_div.sort_values(by=['Stock', 'StartDate', 'EndDate'])
df_div#.head(1)  # Display the first few rows to check the result
### GET VALUES FOR BUILDING DIVIDENDS 
# GET stocks
oldest_date = df_div['StartDate'].min();
start_date = oldest_date.strftime('%Y-%m-%d')
unique_stocks = df_div['Stock'].unique().tolist()
#print('\n* FIND DIVIDENDS IN THESE STOCKS <unique_stocks> ::: ',unique_stocks,'\n\n* OLDEST START DATE \t\t <start_date>  ::: ',start_date,'\n\ndf_div \n\n')
#print(df_div)#.head(4))

################################

# import pandas as pd
# from datetime import datetime, timedelta

# def adjust_to_thursday(cutoff_date):
#     """
#     Adjust the date to ensure it's suitable for analysis, prioritizing Thursday,
#     or Friday if Thursday isn't an option.
    
#     :param cutoff_date: The original cutoff date.
#     :return: Adjusted date.
#     """
#     # Adjust based on the specified date's weekday
#     if cutoff_date.weekday() == 6:  # Sunday
#         return cutoff_date - timedelta(days=3)  # Previous Thursday
#     elif cutoff_date.weekday() == 5:  # Saturday
#         return cutoff_date - timedelta(days=2)  # Previous Thursday
#     elif cutoff_date.weekday() in [0, 1, 2, 3]:  # Monday to Thursday
#         return cutoff_date + timedelta(days=(3 - cutoff_date.weekday()))
    
#     return cutoff_date

# def filter_df_by_date(df, input_date, date_column):
#     """
#     Filter a dataframe to exclude data after a specific date based on a date column.
#     Adds columns with the current run date and the input date as the cutoff.
    
#     :param df: DataFrame to filter.
#     :param input_date: Specific date to use as the cutoff.
#     :param date_column: Name of the column containing date information.
#     :return: Filtered DataFrame.
#     """
#     # Ensure the date column and input_date are in datetime format
#     df[date_column] = pd.to_datetime(df[date_column])
#     cutoff_date = pd.to_datetime(input_date)

#     # Filter the DataFrame to exclude data after the cutoff date
#     filtered_df = df[df[date_column] < cutoff_date].copy()  # Explicit copy to avoid SettingWithCopyWarning

#     # Calculate today's date for the 'run_date' column
#     today = datetime.today()

#     # Add new columns
#     filtered_df['run_date'] = today.strftime('%Y-%m-%d')  # The date when the function is run
#     filtered_df['count_back_from_date'] = cutoff_date.strftime('%Y-%m-%d')  # The specific cutoff date provided

#     return filtered_df

# # Example usage
# # Assuming 'df' is your DataFrame and 'transaction_date' is the date column:
# # filtered_df = filter_df_by_date(df, '2023-12-31', 'transaction_date')

# import pandas as pd

# # Define the function to compare and create 'AnalysisEndDate'
# def compare_and_set_analysis_end_date(df):
#     # Ensure both columns are in datetime format
#     df['EndDate'] = pd.to_datetime(df['EndDate'])
#     df['count_back_from_date'] = pd.to_datetime(df['count_back_from_date'])
    
#     # Adjust the condition as per the new requirement
#     df['AnalysisEndDate'] = df.apply(lambda row: row['count_back_from_date'] if row['count_back_from_date'] < row['EndDate'] else row['EndDate'], axis=1)
#     return df





# ########################################################################################################################################################
