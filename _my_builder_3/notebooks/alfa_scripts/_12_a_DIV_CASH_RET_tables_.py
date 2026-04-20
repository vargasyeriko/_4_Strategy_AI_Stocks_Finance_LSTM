df = get_df_ledger()
############################## 
# ############################################
# ############################################
# ############################################
# ############################################
# ############################################ ADD ONS -> COSTS
df_br_costs = export_ladger_get_costs(df)
br_costs_total = df_br_costs['trans_fee'].sum()
#df_br_costs
print(f'\nBROCKAGE COSTS till {d_start_date} are $ {br_costs_total}\n')
# ############################################
# ############################################
# ############################################
# ############################################
# ############################################ ADD ONS -> 
df_div =to_df_div(df) # fn from __0_b_fns_PORTFOLIO_updt

# ############################################
# ############################################ ADD ONS -> 

df_master = create_master_df(df_div, d_start_date)
#input('')
############################################################## DIVIDENDS
# Grouping by 'Stock' and 'period', then calculating the sum of 'Dividends'
dividends_sum = df_master.groupby(['Stock', 'period'])['Dividends'].sum().reset_index()
# Renaming the summed column
dividends_sum.rename(columns={'Dividends': 'total_divs'}, inplace=True)
# Merging the summed dividends back to the original dataframe
df_master = pd.merge(df_master, dividends_sum, on=['Stock', 'period'], how='left')

################################ filtered DF  : df_add_divs : Stock, period, total_divs
df_add_divs= df_master.copy()
# # Dropping duplicates, keeping the last entry (most recent 'AnalysisEndDate') per 'Period' and 'Stock'
df_add_divs.sort_values(by=['period', 'AnalysisEndDate'], inplace=True)
df_add_divs = df_add_divs.drop_duplicates(subset=['period', 'Stock'], keep='last')
df_add_divs = df_add_divs[['Stock', 'period','total_divs']].copy()

############################################################# filtered DF RETURNS ,
#no 0 units start, keep upddated 
#df_master work ::: FIRST DELETE ALL the rows where units =0 and d_start_date = Startdate
mask = (df_master['units_hold'] == 0.0000) & (df_master['StartDate'] == d_start_date).copy()
deleted_count = mask.sum().copy()  # prints how many rows it will delete
df_ret = df_master[~mask].copy()  # removes rows where the mask is True

############ now keep only the rows where Stock has the latest AnalysisEndDate
df_ret.sort_values(by=['period', 'AnalysisEndDate'], inplace=True)
# Dropping duplicates, keeping the last entry (most recent 'AnalysisEndDate') per 'Period' and 'Stock'
df_ret = df_ret.drop_duplicates(subset=['period', 'Stock'], keep='last').copy()

##################### fetch prices by period 
df_ret['price_end_date'] = df_ret.apply(
    lambda row: fetch_stock_price_on_date_close(row['Stock'], row['AnalysisEndDate'], df_close), axis=1)

#print(df_master[['Stock', 'AnalysisEndDate', 'price_end_date']])
##################### ##################### #####################  Merge df_add_divs & df_ret
# Initialize an empty DataFrame to store the combined results
df_report = pd.DataFrame()
# Iterate through each unique period available in df_add_divs
for period in df_add_divs['period'].unique():
    # Filter df_master and df_add_divs for the current period
    df_master_period = df_ret[df_ret['period'] == period].copy()
    df_add_divs_period = df_add_divs[df_add_divs['period'] == period]
    
    # Merge the DataFrames
    df_combined = df_add_divs_period.merge(df_master_period, on='Stock', how='outer', suffixes=('', '_master'))
    
    # Set 'AnalysisEndDate' from df_master_period if available
    if not df_master_period.empty:
        common_analysis_end_date = df_master_period['AnalysisEndDate'].iloc[0]
    else:
        common_analysis_end_date = 'No Date'  # Define a default if df_master_period is empty

    # Fill missing values in 'AnalysisEndDate' and other columns
    df_combined['AnalysisEndDate'].fillna(common_analysis_end_date, inplace=True)
    df_combined['total_divs'].fillna(0, inplace=True)

    # Fill other necessary defaults
    for column in df_combined.columns:
        if 'master' in column:  # Columns from df_master_period might have suffix '_master'
            clean_column = column.replace('_master', '')
            df_combined[clean_column].fillna(df_combined[column], inplace=True)
            df_combined.drop(column, axis=1, inplace=True)  # Drop master columns after filling
        elif df_combined[column].dtype == 'float64':
            df_combined[column].fillna(0, inplace=True)
        elif df_combined[column].dtype == 'object' and column.endswith('Date') and column != 'AnalysisEndDate':
            df_combined[column].fillna('No Date', inplace=True)  # or a specific default date if needed

    # Append the combined DataFrame of the current period to the final DataFrame
    df_report = pd.concat([df_report, df_combined], ignore_index=True)

# Reset index in the final DataFrame to ensure unique indexing
df_report.reset_index(drop=True, inplace=True)

df_report = df_report[['Stock', 'units_hold', 'AnalysisEndDate', 'period',
                      'price_end_date','total_divs']].copy()

## FINALLY GET holding value per Stock
df_report['stock_value_hold'] = df_report['units_hold'] * df_report['price_end_date']

# SORT
df_report = df_report.sort_values(by=['period','Stock'])

# until here that lenght :: print(len(df_report)) / n of periods  should be equal to all stock no. in hist

######################## df_report has monthly dividends and returns hoding value. there are 0 in prices that were not in df_ret
######################################### ADD CASH :::
name_cash_init_modif  = '_df_cash_init_1_empty_CASH'
df_cash = pd.read_pickle(f'_20_add_cash/{name_cash_init_modif}.pkl')

# New column initialization
df_report['period_cash'] = 0.0

# Iterate over df_report and update 'cash' based on conditions
for index, row in df_report.iterrows():
    # Summing amounts where DateTrans is less than AnalysisEndDate
    sum_amount = df_cash[(df_cash['DateTrans'] < row['AnalysisEndDate'])]['amount'].sum()
    df_report.at[index, 'period_cash'] = sum_amount

######################################### make a few last adjustments :::: 
##### ***** 1 # GET total DIVS by period (the stock dividend amount is in total_divs), and 

# Group by 'period' and sum 'total_divs', then merge this back to the original df_report
total_divs_by_period = df_report.groupby('period')['total_divs'].sum().reset_index()
total_divs_by_period.rename(columns={'total_divs': 'period_divs'}, inplace=True)

# Merge this aggregated data back to the original DataFrame
df_report = pd.merge(df_report, total_divs_by_period, on='period', how='left')


##### ***** 1.2 get period cash excess = (period_cash	 + period_divs)
df_report['period_total_cash'] = df_report['period_cash'] + df_report['period_divs']


##### ***** 2 # GET total stock  HOLDING value , and period holding value 
# Group by 'period' and sum 'stock_value_hold', then merge this back to the original df_report
total_stock_value_by_period = df_report.groupby('period')['stock_value_hold'].sum().reset_index()
total_stock_value_by_period.rename(columns={'stock_value_hold': 'period_stocks_value'}, inplace=True)

# Merge this aggregated data back to the original DataFrame
df_report = pd.merge(df_report, total_stock_value_by_period, on='period', how='left')


##### ***** 3 # GET TOTAL portfolio holding Value 
df_report['period_total_holds'] = df_report['period_total_cash'] + df_report['period_stocks_value']


########## 4 final adjustments and pivot tables :::
# round 
columns_to_round = [
    'units_hold', 'price_end_date', 'total_divs',
    'stock_value_hold', 'period_divs','period_total_cash', 
    'period_stocks_value','period_total_holds']

for column in columns_to_round:
    if column in df_report.columns:  # Check if column exists to prevent errors
        # Apply rounding directly
        df_report[column] = df_report[column].apply(lambda x: round(x, 2) if pd.notnull(x) else x)
##################################################
df_report = df_report.merge(df_br_costs, on='period', how='left').copy()
df_report.head()
df_report.to_pickle(f'_1_tables/_df_report_3_ret_div_cash_.pkl')

##################################################
df = df_report.copy()
##################################################
##################################################

##################################################

##################################################

################################################## DOWN BELOW JUST FNS !!


#df = pd.read_pickle(f'_1_tables/_df_report_3_ret_div_cash_.pkl')
    
def get_units_percentages(df):
    import pandas as pd
    
    # df is the main DataFrame, select a few necessary columns
    df_pies = df[['Stock', 'AnalysisEndDate', 'period', 'stock_value_hold', 
                  'period_cash','period_divs','period_total_cash', 'trans_fee']]
    
    # Determine unique periods
    unique_periods = sorted(df['period'].unique())
    
    # Initialize an empty DataFrame to collect final results
    df_final = pd.DataFrame()
    
    # Iterate over each period
    for period in unique_periods:
        # Filter by current period
        df_current = df_pies[df_pies['period'] == period]
    
        # Extract the first value from period_total_cash column (assuming all are the same)
        cash_value = df_current['period_total_cash'].iloc[0]
        analysis_end_date = df_current['AnalysisEndDate'].iloc[0]  # Same date for all entries in df_current
        trans_fee = df_current['trans_fee'].iloc[0]  # Same transaction fee for all entries in df_current
    
        # Create a new DataFrame to append
        new_row = pd.DataFrame({
            'Stock': ['CASH'],
            'AnalysisEndDate': [analysis_end_date],
            'period': [period],
            'stock_value_hold': [cash_value],
            'period_total_cash': [cash_value],  # This might be redundant but included for consistency
            'trans_fee': [trans_fee]
        })
    
        # Append the new row to df_current
        df_current = pd.concat([df_current, new_row], ignore_index=True)
    
        # Find the index of the 'CASH' row
        cash_index = df_current[df_current['Stock'] == 'CASH'].index[0]
    
        # Subtract the trans_fee from the stock_value_hold for the 'CASH' row
        df_current.loc[cash_index, 'stock_value_hold'] -= df_current.loc[cash_index, 'trans_fee']
    
        # Calculate the total of stock_value_hold for percentage calculation
        total_stock_value = df_current['stock_value_hold'].sum()
    
        # Calculate percentages in the stock_value_hold column
        df_current['stock_value_hold_pct'] = (df_current['stock_value_hold'] / total_stock_value) * 100
    
        # Select the columns for the final DataFrame
        df_current_pie = df_current[['Stock', 'AnalysisEndDate', 'period', 'stock_value_hold',
                                     'period_cash','period_divs','stock_value_hold_pct', 'trans_fee']]
    
        # Append the processed DataFrame to the final DataFrame
        df_final = pd.concat([df_final, df_current_pie], ignore_index=True)
    
    # Resulting DataFrame
    df_final.head(49)
    return df_final
    


##################################################

##################################################

#df_report.to_pickle(f'_1_tables/_df_report_3_ret_div_cash_.pkl')
#print('\n ATTN ! tbls > df_report EXPORTED \n')

# # Aggregate 'Dividends' by 'Stock' and 'period 
# aggregated_data = df_master.groupby(['Stock', 'period'])['Dividends'].sum().reset_index()
# # Pivot the table to see 'Dividends' for each 'period ' by 'Stock'
# div_pivot_table_master = aggregated_data.pivot(index='Stock', columns='period', values='Dividends').fillna(0)