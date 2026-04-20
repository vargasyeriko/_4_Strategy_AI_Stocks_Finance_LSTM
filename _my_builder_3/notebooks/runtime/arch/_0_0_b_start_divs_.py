# import pandas as pd
# import glob
# import pandas as pd
# import numpy as np
# import yfinance as yf
# from datetime import datetime, timedelta
# from _fns import fetch_dividend_analysis
# # Here build 
# # 1 - every time you run it check price in last month and update if necessary 
# # 2 - new stocks are added ... 


# ### ############################################################################
# ### ############################################################################
# ### ############################################################################
# ### ############################################################################
# ### ############################################################################
# def fetch_fields():
#     import pandas as pd
#     import glob
#     import pandas as pd
#     import numpy as np
#     import yfinance as yf
#     from datetime import datetime, timedelta
#     ### ############################################################################

#     portfolio_labels_g = ['AMC.AX', 'ALD.AX', 'ANZ.AX', 'APA.AX', 'BHP.AX','SQ2.AX', 'BXB.AX', 'CHC.AX', 'COL.AX', 'CBA.AX', 
#                         'CSL.AX', 'CSR.AX', 'IAG.AX', 'JLG.AX', '360.AX',
#                         'PXA.AX', 'RHC.AX', 'RMD.AX', 'SHL.AX', 'TLS.AX', 
#                         'TCL.AX', 'EX20.AX', 'WES.AX', 'VCX.AX', 'XRO.AX',
#                         'QUAL.AX', 'ANN.AX', 'GLOB.AX', 'FEMX.AX', 'MCSI.XA',
#                         'CLDD.AX','DJRE.AX', 'ACDC.AX']
#     ############################################################################
#     #
#     ############################################################################
#     # history 
#     df_columns = ['Stock', 'PercentSold', 'keep_drop', 'trans_type', 'DateTrans','exchange_stocks','sell_perc']
#     hist_df_g = pd.DataFrame(columns=df_columns)  # Initialize with the updated columns
    
#     # The data to append as a DataFrame, now excluding 'AmountSold' and 'AmountBought' # history of sells
#     data_to_append_df = pd.DataFrame([
#         {'Stock': 'SQ2.AX', 'PercentSold': 30.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2022-10-27','exchange_stocks': ['RHC.AX'] ,'sell_perc': [100]},
#         {'Stock': 'CBA.AX', 'PercentSold': 25.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2022-12-01','exchange_stocks':['IAG.AX']  ,'sell_perc': [100]},
#         {'Stock': 'BHP.AX', 'PercentSold': 19.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-03-10','exchange_stocks': ['TCL.AX']  ,'sell_perc': [100]}, 
#         {'Stock': 'BXB.AX', 'PercentSold': 15.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-03-10','exchange_stocks':['TCL.AX']  ,'sell_perc': [100]},
#         {'Stock': 'JLG.AX', 'PercentSold': 15.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-03-10','exchange_stocks':['TCL.AX']  ,'sell_perc': [100]},
    
#         {'Stock': 'EX20.AX', 'PercentSold': 50.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-03-13','exchange_stocks':['VHY.AX']  ,'sell_perc': [100]},
#         {'Stock': 'QUAL.AX', 'PercentSold': 30.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-03-10','exchange_stocks':['FEMX.AX']  ,'sell_perc': [100]},
#         {'Stock': 'CSL.AX', 'PercentSold': 38.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-07-20','exchange_stocks':['SHL.AX']  ,'sell_perc': [100]},  
#         {'Stock': 'DJRE.AX', 'PercentSold': 100.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-07-20','exchange_stocks':['IJH.AX', 'ANZ.AX']  ,'sell_perc': [50, 50]},
#         {'Stock': 'ACDC.AX', 'PercentSold': 100.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-07-20','exchange_stocks':['TSLA']  ,'sell_perc': [100]},
        
#         {'Stock': 'FEMX.AX', 'PercentSold': 50.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-09-11','exchange_stocks':['TLS.AX', 'CSR.AX']  ,'sell_perc': [33, 67]},
       
#         {'Stock': 'CLDD.AX', 'PercentSold': 15.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-10-10','exchange_stocks':['CASH','TSLA']  ,'sell_perc': [70, 30]},
#         {'Stock': 'QUAL.AX', 'PercentSold': 15.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-10-10','exchange_stocks':['CASH','TSLA']  ,'sell_perc': [70, 30]},
    
#         {'Stock': 'ANN.AX', 'PercentSold': 100.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2024-01-10','exchange_stocks':['RMD.AX']  ,'sell_perc': [100]},
    
#         {'Stock': 'PXA.AX', 'PercentSold': 100.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2024-02-13','exchange_stocks':['MQG.AX']  ,'sell_perc': [100]},
#         {'Stock': 'VCX.AX', 'PercentSold': 100.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2024-02-13','exchange_stocks':['MIN.AX']  ,'sell_perc': [100]},
#         #{'Stock': 'ANN.AX', 'PercentSold': 23.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2024-02-13','exchange_stocks':['FEMX.AX', 'SHL.AX']  ,'sell_perc': [50, 50]},
    
#         {'Stock': 'CLDD.AX', 'PercentSold': 100.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2024-02-13','exchange_stocks':['SEMI.AX']  ,'sell_perc': [100]},
    
    
#     ])
    
#     hist_df_g = pd.concat([hist_df_g, data_to_append_df], ignore_index=True)
    
#     ###################################################################################

#     portfolio_labels_d = ['DHOF.AX', 'ILB.AX', 'QPON.AX', 'TACT.XA', 'GROW.AX', 
#                         'MVA.AX', 'GOLD.AX'] # million 
    
#     #print(portfolio_percentages)
#     ############################################################################
    
#     import pandas as pd
#     from datetime import datetime
    
#     df_columns = ['Stock', 'PercentSold', 'keep_drop', 'trans_type', 'DateTrans','exchange_stocks','sell_perc']
#     hist_df_d = pd.DataFrame(columns=df_columns)  # Initialize with the updated columns
    

    
#     data_to_append_df = pd.DataFrame([
#         {'Stock': 'TACT.XA', 'PercentSold': 25.0, 'keep_drop': 'd', 'trans_type': 's',
#          'DateTrans': '2023-05-03','exchange_stocks': ['ILB.AX'] ,'sell_perc': [100]},
        
#         {'Stock': 'GOLD.AX', 'PercentSold': 66.0, 'keep_drop': 'd', 'trans_type': 's', 
#          'DateTrans': '2023-07-20','exchange_stocks':['QPON.AX']  ,'sell_perc': [100]}, 
#         # updt sell %66
        
#         {'Stock': 'MVA.AX', 'PercentSold': 100.0, 'keep_drop': 'd', 'trans_type': 's', 
#          'DateTrans': '2023-09-11','exchange_stocks': ['QPON.AX', 'ILB.AX']  ,'sell_perc': [50, 50]},
        
#         {'Stock': 'QPON.AX', 'PercentSold': 23.0, 'keep_drop': 'd', 'trans_type': 's', 
#          'DateTrans': '2024-02-13','exchange_stocks':['HCRD.AX', 'USIG.AX']  ,'sell_perc': [35, 65]},
        
#         {'Stock': 'ILB.AX', 'PercentSold': 35.0, 'keep_drop': 'd', 'trans_type': 's', 
#          'DateTrans': '2024-02-13','exchange_stocks':['HCRD.AX', 'USIG.AX']  ,'sell_perc': [50, 50]},
#         # updt sell %35
        
        
#         {'Stock': 'DHOF.AX', 'PercentSold': 50.0, 'keep_drop': 'd', 'trans_type': 's', 
#          'DateTrans': '2024-02-13','exchange_stocks':['HCRD.AX']  ,'sell_perc': [100]},
        
#     ])
    
#     hist_df_d = pd.concat([hist_df_d, data_to_append_df], ignore_index=True)
#     #########################################################################
#     # CASH EXCESS
#     data = {
#         'date_cash_to_stock': ['2024-02-13'],
#         'per_cash_to_stock': [30 ],
#         'stock_from_cash': ['BUGG.AX']
#     }
#     df_ce_start = pd.DataFrame(data)
    
#     df_ce_start.to_pickle(f'_12_tables_ce/_ce_start.pkl')
    
#     data = {
#         'date_cash_to_stock': ['2024-02-13'],
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



# # import pandas as pd
# # import yfinance as yf

# # # Initialize a cache for dividends to avoid redundant network calls
# # dividend_cache = {}

# # def get_cached_dividends(stock):
# #     if stock not in dividend_cache:
# #         ticker = yf.Ticker(stock)
# #         dividends = ticker.dividends
# #         dividends.index = dividends.index.tz_localize(None)  # Ensure timezone-naive
# #         dividend_cache[stock] = dividends
# #     return dividend_cache[stock]

# # def add_custom_dividends(stock, start_date, end_date, frequency='M', dividend_amount=0.155):
# #     if stock == 'TACT.XA':  # Example to add manual dividends for a specific stock
# #         dates = pd.date_range(start=start_date, end=end_date, freq=frequency) + pd.tseries.offsets.MonthEnd(0)
# #         dividends = pd.Series(dividend_amount, index=dates)
# #         return dividends
# #     return pd.Series([])  # Return an empty series for other stocks

# # def fetch_dividend_analysis(l_stocks_updt, start_date, end_date=None, custom_dividends=True):
# #     # Setting up end date
# #     end_date = end_date or pd.Timestamp.today().normalize()
    
# #     # Create a dictionary to hold dividend data
# #     dividend_data = {}
    
# #     # Fetch or generate dividend data for each stock
# #     for stock in l_stocks_updt:
# #         if custom_dividends and stock == 'TACT.XA':
# #             dividend_data[stock] = add_custom_dividends(stock, start_date, end_date)
# #         else:
# #             dividend_data[stock] = get_cached_dividends(stock)[start_date:end_date]
    
# #     # Convert dictionary into DataFrame
# #     df_dividends = pd.DataFrame(dividend_data)
    
# #     # Fill missing dates with 0
# #     df_dividends.fillna(0, inplace=True)
    
# #     # Save the DataFrame to a pickle file
# #     file_path = '_1_fetch/_1_fetched_stock_dividend_percentages.pkl'
# #     df_dividends.to_pickle(file_path)
# #     print(f"Table has been written as '{file_path}'")



# l_stocks_updt = fetch_fields()
# d_start_date = '2022-07-01'
# fetch_dividend_analysis(l_stocks_updt, d_start_date)

# #dividends_df = pd.read_pickle('_1_fetch/_1_fetched_stock_dividend_percentages.pkl')

# ################################################# get AGREGATES do functions for those :::
# # import pandas as pd
# # print(' AGREGATE dividends since INCEPTION ::: \n\n')
# # def process_dividend_data(file_path):
# #     # Load the dividend DataFrame from a pickle file
# #     dividends_df = pd.read_pickle(file_path)
    
# #     # Check if the index is named, if not, name it 'Date'
# #     if dividends_df.index.name is None:
# #         dividends_df.index.name = 'Date'
    
# #     # Reset the index to bring the date into a column
# #     dividends_melted = dividends_df.reset_index().melt(id_vars=['Date'], var_name='Stock', value_name='Dividends')
    
# #     # Aggregate the dividends by stock
# #     dividends_aggregated = dividends_melted.groupby('Stock')['Dividends'].sum()
    
# #     # Display the aggregated dividends
# #     print('\n\n', dividends_aggregated)

# # # Specify the path to your dividend data pickle file
# # file_path = '_1_fetch/_1_fetched_stock_dividend_percentages.pkl'

# # # Call the function to process and display the dividend data
# # process_dividend_data(file_path)

# # ############### custom function 

# # import pandas as pd
# # from datetime import datetime

# # def process_dividend_data(file_path):
# #     # Load the dividend DataFrame from a pickle file
# #     dividends_df = pd.read_pickle(file_path)

# #     # Ask for the start date
# #     start_input = input("Press Enter to use the default start date (earliest date in data), or type 'cd' for custom dates: ")
# #     if start_input.lower() == 'cd':
# #         start_date = input("Enter the start date (YYYY-MM-DD): ")
# #     else:
# #         start_date = dividends_df.index.min()

# #     # Ask for the end date
# #     end_input = input("Press Enter to use today's date as the end date, or type 'cd' for a custom date: ")
# #     if end_input.lower() == 'cd':
# #         end_date = input("Enter the end date (YYYY-MM-DD): ")
# #     else:
# #         end_date = datetime.today().strftime('%Y-%m-%d')

# #     # Ensure the index is named, if not, name it 'Date'
# #     if dividends_df.index.name is None:
# #         dividends_df.index.name = 'Date'

# #     # Filter the DataFrame for the date range
# #     dividends_df = dividends_df[(dividends_df.index >= start_date) & (dividends_df.index <= end_date)]

# #     # Reset the index to bring the date into a column
# #     dividends_melted = dividends_df.reset_index().melt(id_vars=['Date'], var_name='Stock', value_name='Dividends')
    
# #     # Aggregate the dividends by stock
# #     dividends_aggregated = dividends_melted.groupby('Stock')['Dividends'].sum()
    
# #     # Display the aggregated dividends
# #     print('\nAggregated Dividends from', start_date, 'to', end_date, ':')
# #     print(dividends_aggregated)

# # # Specify the path to your dividend data pickle file
# # file_path = '_1_fetch/_1_fetched_stock_dividend_percentages.pkl'

# # # Call the function to process and display the dividend data
# # process_dividend_data(file_path)



# ### ############################################################################ Dividend table simplified
# # import pandas as pd
# # import yfinance as yf
# # from pandas.tseries.offsets import MonthEnd

# # # Cache for storing dividends data
# # dividend_cache = {}

# # def get_cached_dividends(stock):
# #     if stock not in dividend_cache:
# #         ticker = yf.Ticker(stock)
# #         dividends = ticker.dividends
# #         dividends.index = dividends.index.tz_localize(None)  # Ensure timezone-naive
# #         dividend_cache[stock] = dividends
# #     return dividend_cache[stock]

# # # Function to manually add dividends for TACT.XA
# # def add_manual_dividends_tact(start_date, end_date):
# #     dates = pd.date_range(start=start_date, end=end_date, freq='M') + MonthEnd(0)
# #     dividends = pd.Series(0.155, index=dates)
# #     return dividends

# # # Function to fetch dividends for a DataFrame
# # def fetch_dividend_table(l_stocks_updt, d_start_date):
# #     df = pd.DataFrame({
# #         'Stock': l_stocks_updt,
# #         'StartDate': pd.to_datetime(d_start_date),
# #         'AnalysisEndDate': pd.to_datetime('now')
# #     })

# #     # Calculate dividends
# #     def get_dividends(row):
# #         dividends = get_cached_dividends(row['Stock'])
# #         if row['Stock'] == 'TACT.XA':
# #             tact_dividends = add_manual_dividends_tact('2022-07-01', pd.Timestamp.now())
# #             # Using pd.concat to combine dividends
# #             dividends = pd.concat([dividends, tact_dividends]).sort_index()
        
# #         relevant_dividends = dividends[(dividends.index >= row['StartDate']) & (dividends.index <= row['AnalysisEndDate'])]
# #         return relevant_dividends.sum()

# #     df['Dividends'] = df.apply(get_dividends, axis=1)
# #     # Save the DataFrame
# #     df.to_pickle('_1_fetch/_1_fetched_stock_dividend_percentages.pkl')
# #     print("Table has been written as '_1_fetch/_1_fetched_stock_dividend_percentages.pkl'")

# ##################################################### calc mean dividend monthly 

# # import pandas as pd

# # def calculate_average_dividend(stock_symbol):
# #     # Read the pickle file
# #     file_path = '_1_fetch/_1_fetched_stock_dividend_percentages.pkl'
# #     df_dividends = pd.read_pickle(file_path)
    
# #     # Check if the stock symbol is in the DataFrame
# #     if stock_symbol in df_dividends.columns:
# #         # Calculate the average dividend for the stock
# #         average_dividend = df_dividends[stock_symbol].mean()
# #         print(f"The average dividend percentage received for {stock_symbol} is {average_dividend:.2f}%.")
# #     else:
# #         print(f"Stock symbol '{stock_symbol}' is not in the dividend data.")

# # # Example usage
# # calculate_average_dividend('TACT')
