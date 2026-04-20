import pandas as pd
# MASTER TABLE
#df_report= pd.read_pickle('_1_fetch/_1_fe')

# direc = 'jim_outputs'
# file_name = '_master_table_.xlsx'
# file_path = f'{direc}/{file_name}'
# df_report.to_excel(file_path, index=False) 
#
# DIVS
divs = pd.read_pickle('_1_fetch/_1_fetched_stock_dividend_percentages.pkl')
divs = divs.reset_index().rename(columns={'index': 'date'})
divs['date'] = pd.to_datetime(divs['date'])
divs['date'] = divs['date'].dt.strftime('%b-%d-%Y')
sorted_columns = sorted(divs.columns)
sorted_columns.remove('date')
sorted_columns.insert(0, 'date')
divs = divs[sorted_columns]
#
direc = 'jim_outputs'
file_name = '_yf_FETCHED_dividends_table_.xlsx'
file_path = f'{direc}/{file_name}'
divs.to_excel(file_path, index=False) 
#
# RETURNS
# Load the DataFrame from the pickle file
retu = pd.read_pickle("_1_fetch/_0_fetched_stock_data_prices.pkl")
retu = retu.reset_index().rename(columns={'index': 'date'})
retu['date'] = pd.to_datetime(retu['date'])
retu['date'] = retu['date'].dt.strftime('%b-%d-%Y')
sorted_columns = sorted(retu.columns)
sorted_columns.remove('date')
sorted_columns.insert(0, 'date')
retu = retu[sorted_columns]
#
direc = 'jim_outputs'
file_name = '_yf_FETCHED_prices_table_.xlsx'
file_path = f'{direc}/{file_name}'
retu.to_excel(file_path, index=False) 

# CURRENT UNITS  # STOCK, units today LEDGER



# CASH, costs - LEDGER
# NOW add cash Hist & Brockage Cost
cash = pd.read_pickle("_20_add_cash/_df_cash_init_1_empty_CASH.pkl")
cash =cash[['id_time_buy','amount','DateTrans', 'trans_type']]
### BR costs
df_c = pd.read_pickle('_1_tables/_df_costs_1_3_br_costs.pkl')
df_c_cash= pd.concat([ cash,df_c])
df_c_cash = df_c_cash.reset_index(drop=True)
######### write
direc = 'jim_outputs'
file_name = '_LEDGER_CASH_and_BROCKAGE_costs_.xlsx'
file_path = f'{direc}/{file_name}'
df_c_cash.to_excel(file_path, index=False) 
######################################

# direc = 'jim_outputs'
# file_path = 'output.xlsx'
# df.to_excel(file_path, index=False) 

#
print('5 exported')