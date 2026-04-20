import pandas as pd
import glob
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from _fns import main_stock_table_fetched,fetch_dividend_analysis
# Here build 
# 1 - every time you run it check price in last month and update if necessary 
# 2 - new stocks are added ... 


# ### ############################################################################
# ### ############################################################################
# ### ############################################################################
# ### ############################################################################
# ### ############################################################################
# def fetch_fields(portfolio_labels_g,portfolio_labels_d,
#                 data_to_append_df_g,data_to_append_df_d):
#     import pandas as pd
#     import glob
#     import pandas as pd
#     import numpy as np
#     import yfinance as yf
#     from datetime import datetime, timedelta
#     ### ############################################################################

#     portfolio_labels_g = ortfolio_labels_g 
#     ############################################################################
#     #
#     ############################################################################
#     # history 
#     df_columns = ['Stock', 'PercentSold', 'keep_drop', 'trans_type', 'DateTrans','exchange_stocks','sell_perc']
#     hist_df_g = pd.DataFrame(columns=df_columns)  # Initialize with the updated columns
    
#     The data to append as a DataFrame, now excluding 'AmountSold' and 'AmountBought' # history of sells
#     data_to_append_df = data_to_append_df_g
    
#     hist_df_g = pd.concat([hist_df_g, data_to_append_df], ignore_index=True)
    
#     ###################################################################################

#     portfolio_labels_d = portfolio_labels_d # million 
    
#     #print(portfolio_percentages)
#     ############################################################################
    
#     import pandas as pd
#     from datetime import datetime
    
#     df_columns = ['Stock', 'PercentSold', 'keep_drop', 'trans_type', 'DateTrans','exchange_stocks','sell_perc']
#     hist_df_d = pd.DataFrame(columns=df_columns)  # Initialize with the updated columns
    

    
#     data_to_append_df = data_to_append_df_g
    
#     hist_df_d = pd.concat([hist_df_d, data_to_append_df], ignore_index=True)
#     #########################################################################
#     # CASH EXCESS
#     data = {
#         'date_cash_to_stock': ['2024-02-15'],
#         'per_cash_to_stock': [30 ],
#         'stock_from_cash': ['BUGG.AX']
#     }
#     df_ce_start = pd.DataFrame(data)
    
#     df_ce_start.to_pickle(f'_12_tables_ce/_ce_start.pkl')
    
#     data = {
#         'date_cash_to_stock': ['2024-02-15'],
#         'per_cash_to_stock': [30 ],
#         'Stock': ['BUGG.AX']
#     }
#     df_ce_start = pd.DataFrame(data)
    
#     # after building ask function CE 
    
#     stock_list_ce = df_ce_start['Stock'].tolist()

#     #########################################################################
    
#     hist_df_0 = pd.concat([hist_df_d,hist_df_g], ignore_index=True)
#     #########################################################################
    
    
#     def concat_pkl_to_df(hist_df, directory=""):
#         """
    
#         """
#         # Ensure the directory path ends with a slash
#         directory = directory.rstrip('/') + '/'
    
#         # Find all .pkl files in the specified directory
#         pkl_files = glob.glob(f"{directory}*.pkl")
    
#         # Read each .pkl file and concatenate it to hist_df
#         for file_path in pkl_files:
#             # Read the .pkl file
#             df_entry = pd.read_pickle(file_path)
    
#             # Concatenate the read DataFrame to hist_df
#             hist_df = pd.concat([hist_df, df_entry], ignore_index=True)
#             #hist_df = hist_df.append(df_entry, ignore_index=True)
#         return hist_df
    
#     df_add = concat_pkl_to_df(hist_df_0, directory="_2_tables_add/")
    
#     ######################################
    
#     unique_stocks = set(df_add['Stock'])
#     unique_exchange_stocks = set(x for sublist in df_add['exchange_stocks'] for x in sublist)
#     # Combine both sets to get all unique stocks
#     all_unique_stocks = unique_stocks.union(unique_exchange_stocks)
#     # Convert the set back to a list if needed
#     all_unique_stocks_list_df_add = list(all_unique_stocks)
    
    
#     ######################################
    
#     # join all init 
#     stock_list_all = portfolio_labels_g + portfolio_labels_d + stock_list_ce +all_unique_stocks_list_df_add 
    
#     unique_stocks = list(set(stock_list_all))
#     # GET rid of cash 
#     l_stocks_updt = [stock for stock in unique_stocks if stock != 'CASH']

#     return l_stocks_updt



##################################### 
##################################### 
##################################### 
##################################### 
##################################### 
##################################### GET UPDATED stock list and start date
l_stocks_updt = fetch_fields()

d_start_date = '2022-07-01'
start_date_reset = d_start_date
#print('\n->', len(l_stocks_updt),f'Stocks being fetched from {d_start_date} till today') 

####################################################### Prices

# writes fetched table
#main_stock_table_fetched(l_stocks_updt,d_start_date)    
              
########################################################## dividends

# writes fetched table
#fetch_dividend_analysis(l_stocks_updt, d_start_date)

############################################################### END
##################################### 
##################################### 
##################################### 
#####################################
import pandas as pd
from datetime import datetime, timedelta

def to_fetch_check(l_stocks_updt,d_start_date,start_date_reset):
    
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
        d_start_date = start_date_reset
    else:
        print("The last date in the DataFrame is today's date and the data is valid. No action needed.")
        return 