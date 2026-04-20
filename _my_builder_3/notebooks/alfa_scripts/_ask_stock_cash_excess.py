import pandas as pd
exec(open(f"_fns_ask.py",encoding="utf-8").read())
d_start_date ,total_inv,start_date_reset = init_inv_dates()
d_start_date = datetime.strptime("2022-01-01", "%Y-%m-%d")  # Modify the date as needed

now = datetime.now()

df= pd.read_pickle(f'_1_tables/_df_0_init_UNITS.pkl')
stock_names  = sorted(df['Stock'])#.tolist()[:-2] 

trans_date = '2023-02-12'#input_date_and_confirm()
print("Your entered date is:", trans_date);trans_date_input = trans_date


try:
    # Convert the input string to a datetime object
    trans_date = datetime.strptime(trans_date_input, "%Y-%m-%d")

    # Print the entered date
    print("Your entered date is:", trans_date.strftime("%Y-%m-%d"))

    # Check if the date is within the valid range
    if d_start_date <= trans_date <= datetime.now():
        print("The transaction date is valid.")
        ce_stocks   = stock_transaction_exchange(stock_names)
        ce_percents ,df_ce_add = allocate_percentages_to_stocks_ce(ce_stocks, trans_date)
        print(df_ce_add)
        
    else:
        print("You are attempting to write a transaction outside of the interval date portfolio since inception. RE-START ! ")
        stock_names  = []

except ValueError:
    print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

input('')


# ## IF NO SELECTION
# if rsp_updt != 'n':


#     update_df_with_selections_exchange(df_drop,stock_names)
#     # and contains a 'selected_stocks' column filled with selected stock names.===========================
#     df_drop = allocate_percentages_to_stocks(df_drop)

#     import ast

#     # Assuming df is your DataFrame
#     # Convert the string representation of a list to an actual list
#     df_drop['selected_stocks'] = df_drop['selected_stocks'].apply(ast.literal_eval)
#     # RENAME VARIABLES

#     # Assuming 'df' is your DataFrame
#     df_drop.rename(columns={'selected_stocks': 'exchange_stocks', 'allocation_percentages': 'sell_perc'}, inplace=True)

#     df_drop['id_time'] = df_drop['Stock'] + "_" + df_drop['DateTrans'] + "_" + df_drop['trans_type']
#     df_drop['DateTrans'] = pd.to_datetime(df_drop['DateTrans'])
#     df_drop['DateTrans'] = df_drop['DateTrans'].dt.strftime('%Y-%m-%d')

#     stock_new = df_drop.iloc[0,0][0:2]
#     transtype_new = df_drop.iloc[0,4]
#     print(f' \n\n  {df_drop}')
#     print('\n\n ATTN : Are you sure you want to write this new entry to the tables_add?')
#     rsp_updt = input('\n  ... y ... TO WRITE to tables and RUN updates  << or >> PRESS ENTER to EXIT \n\n')

#     print(' *\n*\n* ')
#     if rsp_updt == 'y':
#         df_drop.to_pickle(f'_2_tables_add/_{stock_new}_{transtype_new}_type_HistAddNew_on_{formatted_date_time}.pkl')
#         #    HISTORY
#         print(f'\n*\n* ADDED !!! \n\n')

#     else :
#         print('EXITING ... \n\n')



############################################################################
############################################################################
# df and df_add to do the whole stock accomodation 
#df_add['DateTrans'] = df_add['DateTrans'].dt.strftime('%Y-%m-%d')

############################################################################
############################################################################

############################################################################
############################################################################

############################################################################
############################################################################




############################################################################
############################################################################

############################################################################
############################################################################

############################################################################
############################################################################

############################################################################
############################################################################




############################################################################
############################################################################

############################################################################
############################################################################

############################################################################
############################################################################

############################################################################
############################################################################


