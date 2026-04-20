

#print('RETURNS :::\n')
# EXPORT DIVIDENDS RETURNS 5
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

from _fns import fetch_stock_price_on_date_close

import pandas as pd
df_close = pd.read_pickle("_1_fetch/_0_fetched_stock_data_prices.pkl")
# Ensure that the index is of datetime type if it isn't already
if not pd.api.types.is_datetime64_any_dtype(df_close.index):
    df_close.index = pd.to_datetime(df_close.index)




nme_df_hist_unit_divs = '_df_hist_12_up_to_date_DIV-UNITS' 
nme_df_master = '_df_periods_123_monthly_df_HIST_'
nme_cash_init_modif  = '_df_cash_init_1_empty_CASH'



# df_master
df_master = pd.read_pickle(f'_1_tables/{nme_df_master}.pkl')
df_master['AnalysisEndDate'] = pd.to_datetime(df_master['AnalysisEndDate'])

# cash bal
name_cash_init_modif  = '_df_cash_init_1_empty_CASH'
df_cash    = pd.read_pickle(f'_20_add_cash/{nme_cash_init_modif}.pkl')


##############################################################
##############################################################
# get rid where the units are 0 
# Create a new DataFrame with rows where unit_hold equals 0.0
df_filtered = df_master[df_master['units_hold'] == 0.0]

# Update df_master to exclude rows where unit_hold equals 0.0
df_master = df_master[df_master['units_hold'] != 0.0]

periods = df_master['m_period'].unique()
dfs = {}

for period in periods:
    temp_df = df_master[df_master['m_period'] == period].copy()

    temp_df['closing_price'] = temp_df.apply(lambda row: fetch_stock_price_on_date_close(row['Stock'], 
                                                    row['AnalysisEndDate'], 
                                                    df_close), axis=1)

    temp_df['holding_value'] = temp_df['units_hold'] * temp_df['closing_price']
    
    dfs[period] = temp_df

#print('\n Quick Summary \n')
# At this point, dfs contains separate dataframes for each m_period, with closing prices and holding cash calculated.

# ##############################################################
# ##############################################################
# ##############################################################
# df_cash = pd.read_pickle('_1_tables/_3_up_to_date_cash_bal_.pkl')


##############################################################
##############################################################
##############################################################
##############################################################import numpy as np

###############################################################
# Your existing dfs dictionary
dfs = {
    '0m': dfs['0m'],
    '3m': dfs['3m'],
    '6m': dfs['6m'],
    '12m': dfs['12m']
}

# Initialize an empty DataFrame for the summary
df_ret = pd.DataFrame(columns=['Period', 'TotalHoldingValue', 'TotalDiv', 'AnalysisEndDate'])

summary_data = []  # Create an empty list to store data dictionaries

# Loop through each key (period) and corresponding DataFrame to summarize
for period, df in dfs.items():
    # Ensure 'AnalysisEndDate' is the same for all rows in the DataFrame
    analysis_end_date = df['AnalysisEndDate'].iloc[0]
    # Sum the 'holding_value' column
    total_holding_value = df['holding_value'].sum()
    
    # Sum the 'dividend_total' column
    total_dividends = df['dividend_total'].sum()
    
    # Append to the summary list as a dictionary
    summary_data.append({
        'Period': period,
        'TotalHoldingValue': total_holding_value,
        'TotalDiv': total_dividends,
        'AnalysisEndDate': analysis_end_date
    })

# Convert the list of dictionaries to a DataFrame and concatenate it to the existing df_ret
df_ret = pd.concat([df_ret, pd.DataFrame(summary_data)], ignore_index=True)

# This will print out the summary DataFrame
#print(df_ret)


################################################## CASH

def append_cash_amount(df_ret, df_cash):
    # Convert 'AnalysisEndDate' in df_ret and 'DateTrans' in df_cash to datetime, using errors='coerce'
    df_ret['AnalysisEndDate'] = pd.to_datetime(df_ret['AnalysisEndDate'], errors='coerce')
    df_cash['DateTrans'] = pd.to_datetime(df_cash['DateTrans'], errors='coerce')
    
    # Initialize the 'cash' column with 0
    df_ret['cash'] = 0.0

    # Iterate over each row in df_ret using iterrows()
    for index, row in df_ret.iterrows():
        analysis_end_date = row['AnalysisEndDate']
        
        # Filter df_cash for entries on or before the analysis_end_date
        filtered_df_cash = df_cash[df_cash['DateTrans'] <= analysis_end_date]
        
        # Sum the 'amount' column of the filtered df_cash, rounding to 2 decimal places
        total_cash = filtered_df_cash['amount'].sum().round(2)
        
        # Update the 'cash' column for the current row in df_ret with total_cash
        df_ret.at[index, 'cash'] = total_cash
    
    return df_ret


df_ret = append_cash_amount(df_ret, df_cash)

print(df_ret)
print('\n_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_ RETURNS UPDATED ! ' )

nme_df_ret =  '_df_ret_summary_1234_RETURNS_'
df_ret.to_pickle(f'_1_tables/{nme_df_ret}.pkl')

############################################# write
