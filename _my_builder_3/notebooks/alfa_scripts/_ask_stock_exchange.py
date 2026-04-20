exec(open(f"_fns_ask.py",encoding="utf-8").read())

d_start_date = datetime.strptime("2022-01-01", "%Y-%m-%d") 
now = datetime.now()

# Format the date and time as requested: yyyy_mm_dd_hh
import pandas as pd
df= pd.read_pickle(f'_1_tables/_df_0_init_UNITS.pkl')

# GET PERCENT SOLD 
stock_names  = sorted(df['Stock'])#.tolist()[:-2] 
selected_stock = stock_transaction(stock_names)
df_drop = handle_transaction(selected_stock, df)

# GET DATE

trans_date_input = input_date_and_confirm()
trans_date = datetime.strptime(trans_date_input, "%Y-%m-%d")

if d_start_date <= trans_date <= datetime.now():
    print("Your entered date is:", trans_date)
    rsp_updt = 'y'

else:
    print("You are attempting to write a transaction outside of the interval date portfolio since inception. RE-START ! ")
    rsp_updt = 'n'

# ARRANGE TABLE -> new row entry
df_drop['keep_drop'] = 'd'
df_drop['trans_type'] = 's'
df_drop['DateTrans'] =trans_date 

##### 

## IF NO SELECTION
if rsp_updt != 'n':


    update_df_with_selections_exchange(df_drop,stock_names)
    # and contains a 'selected_stocks' column filled with selected stock names.===========================
    df_drop = allocate_percentages_to_stocks(df_drop)

    import ast

    # Assuming df is your DataFrame
    # Convert the string representation of a list to an actual list
    df_drop['selected_stocks'] = df_drop['selected_stocks'].apply(ast.literal_eval)
    # RENAME VARIABLES

    # Assuming 'df' is your DataFrame
    df_drop.rename(columns={'selected_stocks': 'exchange_stocks', 'allocation_percentages': 'sell_perc'}, inplace=True)
    input('')
    df_drop['id_time'] = df_drop['Stock'] + "_" + df_drop['DateTrans'].astype(str) + "_" + df_drop['trans_type']
    df_drop['DateTrans'] = pd.to_datetime(df_drop['DateTrans'])
    df_drop['DateTrans'] = df_drop['DateTrans'].dt.strftime('%Y-%m-%d')

    stock_new = df_drop.iloc[0,0][0:2]
    transtype_new = df_drop.iloc[0,4]
    print(f' \n\n  {df_drop}')
    print('\n\n ATTN : Are you sure you want to write this new entry to the tables_add?')
    rsp_updt = input('\n  ... y ... TO WRITE to tables and RUN updates  << or >> PRESS ENTER to EXIT \n\n')

    print(' *\n*\n* ')
    if rsp_updt == 'y':
        df_drop.to_pickle(f'_2_tables_add/_{stock_new}_{transtype_new}_type_HistAddNew_on_{formatted_date_time}.pkl')
        #    HISTORY
        print(f'\n*\n* ADDED !!! \n\n')

    else :
        print('EXITING ... \n\n')

############################################################################
############################################################################
# df and df_add to do the whole stock accomodation 
#df_add['DateTrans'] = df_add['DateTrans'].dt.strftime('%Y-%m-%d')