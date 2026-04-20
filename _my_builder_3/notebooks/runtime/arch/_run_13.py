# import pandas as pd



# name_1_a_Cash_Excess_calc = '_1_a_CASH_Excess_calculation'
# nme_df_hist_unit_divs = '_df_hist_12_up_to_date_DIV-UNITS' 
# nme_df_master = '_df_periods_123_monthly_df_HIST_'

# # cash
# nme_cash_init_modif  = '_df_cash_init_1_empty_CASH'

# # UNITS



# df_master_unit_updt = pd.read_pickle(f'_1_tables/_df_0_init_UNITS.pkl').sort_values(by='Stock')
# df_master_unit_updt['DateMostRecentTrans'] = df_master_unit_updt['StartDate'].copy()

# cash 

# name_cash_init_modif  = '_df_cash_init_1_empty_CASH'
# df_cash_bal    = pd.read_pickle(f'_20_add_cash/{name_cash_init_modif}.pkl')
# df_cash_bal

# DIVIDENDS tables on the making ... see df_div and df for it
#exec(open(f"_12_a_DIV_tables.py",encoding="utf-8").read())

from _fns import calculate_and_add_dividends



import pandas as pd



df_close = pd.read_pickle("_1_fetch/_0_fetched_stock_data_prices.pkl")
# Ensure that the index is of datetime type if it isn't already
if not pd.api.types.is_datetime64_any_dtype(df_close.index):
    df_close.index = pd.to_datetime(df_close.index)

#print('STARTS run 13 \n\n')

try:

    # Execute _run_11.py in its own namespace
    exec(open("_12_a_DIV_tables_.py").read(), {})
except Exception as e:
    # Print error messages
    print("Error ", e)

try:

    # Execute _run_12.py in its own namespace
    exec(open("_13_a_RETURNS_tables_.py").read(), {}) # does not passes output
    # exec(open("_run_12.py").read(), globals()) # it does passes 

except Exception as e:
    # Print error messages
    print("Error ", e)

try:
    # Execute _run_12.py in its own namespace
    print('')
    exec(open("_13_b_RETURNS_months_.py").read(), {}) # does not passes output
    # exec(open("_run_12.py").read(), globals()) # it does passes 

except Exception as e:
    # Print error messages
    print("Error ", e)



