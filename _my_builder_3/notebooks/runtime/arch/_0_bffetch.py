# import pandas as pd
# import glob
# import os

# from datetime import datetime
# now = datetime.now();formatted_date_time = now.strftime("%Y_%m_%d_h%Hm%M")

# from _fns import concat_pkl_to_df ,get_unique_stocks,master_fetch_check
# from _fns import main_stock_table_fetched,fetch_dividend_analysis#,# function 
# from _fns import process_stock_data,fill_missing_values
# from _0_0_all_stocks_ import portfolio_labels_d,portfolio_labels_g , stock_list_ce
# from _0_0_all_stocks_ import data_to_append_df_d,data_to_append_df_g ,df_ce_all_hist


# hist_df_0 = pd.concat([data_to_append_df_g,data_to_append_df_d], ignore_index=True)
# df_add = concat_pkl_to_df(hist_df_0, directory="_2_tables_add/")

# # Get initial UNIQUE STOCK list 
# l_stocks_updt = get_unique_stocks(portfolio_labels_g,portfolio_labels_d,stock_list_ce,df_add)


# # ########## FEtCH !!
# # Creating a DataFrame from the list
# df = pd.DataFrame(l_stocks_updt, columns=['Stock'])
# df.to_pickle(f'_1_fetch/stock_list/_updt_list_{formatted_date_time}.pkl')

# # Check if the file exists
# if not os.path.exists( '_1_fetch/_0_fetched_stock_data_prices.pkl'):
#     # UPDATE STOCKS
#     main_stock_table_fetched(l_stocks_updt, d_start_date)
   
# if not os.path.exists('_1_fetch/_1_fetched_stock_dividend_percentages.pkl'):
#     # UPDATE DIVS
#     fetch_dividend_analysis(l_stocks_updt, d_start_date)

# # ########## FEtCH !! check if days more days has passed or more stocks have been added
# df_close = master_fetch_check(l_stocks_updt,d_start_date)



# import pandas as pd
# import os
# from datetime import datetime

# def update_stock_list(directory):
#     # Get the list of all files in the directory
#     files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.pkl')]
    
#     # If no files are found, return an empty list and print a message
#     if not files:
#         print("No files found in the directory.")
#         return [], []

#     # Find the most recent file based on the modification time
#     latest_file = max(files, key=os.path.getmtime)

#     # Read the DataFrame from the pickle file
#     df = pd.read_pickle(latest_file)

#     # Extract the 'Stock' column into a list
#     l_stock_list_newest_processed = df['Stock'].tolist()

#     # Assuming l_stocks_updt is defined elsewhere and accessible
#     global l_stocks_updt

#     # Find stocks in l_stocks_updt not in l_stock_list_newest_processed
#     _new_stocks = [stock for stock in l_stocks_updt if stock not in l_stock_list_newest_processed]
#     # Check if there are new stocks to add
#     if not _new_stocks:
#         print("No new stocks to add.\n")
#     else:
#         print("New Stocks:", _new_stocks)
#         main_stock_table_fetched(l_stocks_updt, d_start_date)
#         fetch_dividend_analysis(l_stocks_updt, d_start_date)

#     return l_stock_list_newest_processed, _new_stocks

# # Usage example:
# directory = '_1_fetch/stock_list'
# #l_stocks_updt = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN']  # Example list of current stocks
# newest_processed, new_stocks = update_stock_list(directory)
