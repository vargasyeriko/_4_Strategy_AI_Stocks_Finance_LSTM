# from datetime import datetime, timedelta
# def to_df_div(df):
#     # Convert 'DateTrans' and 'StartDate' to datetime type, handling NaT properly
#     df['DateTrans'] = pd.to_datetime(df['DateTrans'], errors='coerce')
#     df['StartDate'] = pd.to_datetime(df['StartDate'], errors='coerce')
    
#     # Identify duplicates based on 'Stock' and 'DateTrans'
#     duplicates = df.duplicated(subset=['Stock', 'DateTrans'], keep=False)
    
#     # Dataframe of duplicates
#     df_duplicates = df[duplicates]
    
#     # Aggregate the duplicates
#     aggregated_duplicates = df_duplicates.groupby(['Stock', 'DateTrans']).agg({
#         'units_updts': 'sum',     # Summing up 'units_updts'
#         'StartDate': 'first',    # Keeping the first 'StartDate'
#         'units_hold': 'first'    # Keeping the first 'units_hold'
#     }).reset_index()
    
#     # Dataframe of non-duplicates
#     df_unique = df[~duplicates]
    
#     df = pd.DataFrame()
#     # Concatenate aggregated duplicates with non-duplicates
#     df = pd.concat([df_unique, aggregated_duplicates], ignore_index=True)
#     df = df.sort_values(by='Stock')
    
#     ####################
#     df_holds = df[df['units_hold'].notna()].copy() #df[df['units_hold'].isna()]
#     #print('init_holds_ledger :\t ', len(df_holds))
    
#     df_updts = df[df['units_hold'].isna()].copy()
#     #print('update_ledger     :\t ',len(df_updts))
    
#     # Convert date columns to datetime
#     df_holds['StartDate'] = pd.to_datetime(df_holds['StartDate'])
#     df_updts['DateTrans'] = pd.to_datetime(df_updts['DateTrans'])
    
#     # Sorting
#     df_updts = df_updts.sort_values(by=['Stock', 'DateTrans'])
    
#     # Function to apply updates and expand DataFrame
#     def update_holds(row):
#         transactions = df_updts[df_updts['Stock'] == row['Stock']]
#         results = []
#         start_date = row['StartDate']
#         units = row['units_hold']
        
#         for _, trans in transactions.iterrows():
#             end_date = trans['DateTrans']
            
#             # Record period before transaction update
#             results.append({'Stock': row['Stock'],
#                             'StartDate': start_date,
#                             'EndDate': end_date,
#                             'units_hold': units})
#             # Update units and set new start date for the next period
#             units += trans['units_updts']
#             start_date = end_date + timedelta(days=1)
        
#         # Append the last period after the last transaction
#         results.append({'Stock': row['Stock'], 
#                         'StartDate': start_date,
#                         'EndDate': pd.to_datetime(datetime.today().strftime('%Y-%m-%d')),
#                         'units_hold': units})
#         return results
    
#     # Applying the updates and expanding DataFrame
#     expanded_rows = df_holds.apply(update_holds, axis=1)
#     df_div = pd.DataFrame([item for sublist in expanded_rows for item in sublist])
    
#     # Check for negative units_hold and print a warning
#     if (df_div['units_hold'] < 0).any():
#         print("Warning: Negative stock holdings detected. Please check the transactions.")
    
#     df_div['StartDate'] = df_div['StartDate'].dt.date
#     df_div['EndDate'] = df_div['EndDate'].dt.date
#     df_div['StartDate'] = pd.to_datetime(df_div['StartDate'])
#     df_div['EndDate'] = pd.to_datetime(df_div['EndDate'])
#     # SORT
#     df_div = df_div.sort_values(by=['Stock', 'StartDate', 'EndDate'])
#     return df_vid

# #######################################