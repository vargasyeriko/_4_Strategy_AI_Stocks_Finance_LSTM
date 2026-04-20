    df = pd.read_pickle(f'_1_tables/_df_report_3_ret_div_cash_.pkl')
    
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
    
