import pandas as pd
######################## NAMES TABLES
#0
df_name_units_updt = '_df_0_init_UNITS'
#1
#2
nme_df_hist_unit_divs = '_df_hist_12_up_to_date_DIV-UNITS' 
#3
nme_df_master = '_df_periods_123_monthly_df_HIST_'
# cash
name_cash_init_modif  = '_df_cash_init_1_empty_CASH'
# 4
nme_df_ret =  '_df_ret_summary_1234_RETURNS_'
###################### READ TABLES
# 0 
df_master_unit_updt =pd.read_pickle(f'_1_tables/{df_name_units_updt}.pkl')
df_master_unit_updt.sort_values(by='Stock')
# 1
# 2
df_hist = pd.read_pickle(f'_1_tables/{nme_df_hist_unit_divs}.pkl')
# 3
df_master = pd.read_pickle(f'_1_tables/{nme_df_master}.pkl')
#df_master = df_master.sort_values(by='dividend_total')
# dfs expand
_df_0m = df_master[df_master['m_period'] == '0m']
_df_3m = df_master[df_master['m_period'] == '3m']
_df_6m = df_master[df_master['m_period'] == '6m']
_df_12m = df_master[df_master['m_period'] == '12m']
# Variables
div_total_0 =_df_0m['dividend_total'].sum()
div_total_3 =_df_3m['dividend_total'].sum()
div_total_6 =_df_6m['dividend_total'].sum()
div_total_12 =_df_12m['dividend_total'].sum()

# 4 df_ret
df_ret = pd.read_pickle(f'_1_tables/{nme_df_ret}.pkl')

# cash
df_cash = pd.read_pickle(f'_20_add_cash/{name_cash_init_modif}.pkl')

# graphs out folder
out_direc = '_0_out'




