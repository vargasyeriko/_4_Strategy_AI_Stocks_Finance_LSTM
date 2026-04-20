# import pandas as pd
# import glob
# import pandas as pd
# import numpy as np
# import yfinance as yf
# from datetime import datetime, timedelta
# from _fns import main_stock_table_fetched
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




# ### ############################################################################ Prices
# l_stocks_updt = fetch_fields()
# d_start_date = '2022-07-01'
# print('\n->', len(l_stocks_updt),f'Stocks being fetched from {d_start_date} till today') 
# #
# main_stock_table_fetched(l_stocks_updt,d_start_date)    # writes fetched table 
# ########################################
# ########################################
# ########################################                

# # # #################################################################################### dividends

