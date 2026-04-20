exec(open(f"_01_a_b_D_G_PORTFOLIO_updt_.py",encoding="utf-8").read())
#
##
#####
df_cash_x_stock = df_ce_all_hist 
df_cash_x_stock =df_cash_x_stock.sort_values(by='date_cash_to_stock').reset_index(drop=True)
# rename  the 'Stock' column and name the new column 'stock_from_cash'
df_cash_x_stock['stock_from_cash'] = df_cash_x_stock['Stock']
###############################################################################################
# Initialize last cutoff date for filtering # Use the smallest possible timestamp
last_cutoff_date = pd.Timestamp.min
#
# Loop through each row in df_cash_x_stock
for index, row in df_cash_x_stock.iterrows():
   
    # ROW cash EXCES variables
    date_cash_to_stock = pd.to_datetime(row['date_cash_to_stock'])

    # READ UNITS df_master
    df = pd.read_pickle(f'_1_tables/{df_name_units_updt}.pkl')
   
    # READ EXCHANGE TRANS HIST df_add
    df_add                 = pd.read_pickle(f'_1_tables/{df_add_name_st_exch}.pkl')    
    df_add['DateTrans']    = pd.to_datetime(df_add['DateTrans'])
    df_add                 = df_add.sort_values(by='DateTrans').reset_index(drop=True)  
    df_add_original_lenght = len(df_add) # get # of trans before cutting df_add    

    # Filter df_add to include only new rows since the last processed date
    df_add = df_add[(df_add['DateTrans'] > last_cutoff_date) & (df_add['DateTrans'] <= date_cash_to_stock)]
    last_cutoff_date = date_cash_to_stock  # Update the last cutoff date
    last_cutoff_date_str = last_cutoff_date.strftime('%Y-%m-%d') #date arrangement
    
    # START UPDATES
    print('\n   ||||||||||||||||||>_ START UPDATES <_||||||||||||||||||||||||\n')
    print(f"Cash Excess ITERATION, to process : {len(df_add)} ",
          f"rows. till date: {date_cash_to_stock.strftime('%Y-%m-%d')} ...")
    df_cash_x_stock_ads = pd.DataFrame([row])

    # check lenght df_add
    len_df_add_in_btw = len(df_add)

    ##############################
        ##############################
        ##############################
    # if you wanted to add CASH injection : here so before Csh Excess see if there are 
    # cash injection -> if there is add it here so it can go to the ledger buy
        ##############################
        ##############################
    ##############################
    if len_df_add_in_btw > 0 :
        filter_cash_excess_check = 1  # MEANS OPEN LOOP FOR UPDTS CASH EXCESS
        # #Correct the use of exec function
        with open(f"{name_updt_ledger_till_ce}.py", "r", encoding="utf-8") as file:
            code = file.read()
            exec(code)
        #print(df)

    ########################### and if no transaction between cash excess movements
    if len_df_add_in_btw == 0 :
        filter_cash_excess_check = 1   # MEANS OPEN LOOP FOR UPDTS CASH EXCESS
        with open(f"{name_updt_no_ledger_ce}.py", "r", encoding="utf-8") as file:
            code = file.read()
            exec(code)
            #start_done = 'yes'
        print('-')

##### FOR EXTRA ROWS after last CASH EXCESS updt
################################################################################
print('\nCASH EXCESS ALGORITHM IS COMPLETELY PROCESSED',
      '\n-------------------------------------------------')
df                  = pd.read_pickle(f'_1_tables/{df_name_units_updt}.pkl')
# READ EXCHANGE TRANS HIST
df_add              = pd.read_pickle(f'_1_tables/{df_add_name_st_exch}.pkl')
df_add['DateTrans'] = pd.to_datetime(df_add['DateTrans'])    
df_add              = df_add.sort_values(by='DateTrans').reset_index(drop=True)  # erase last adde if dont work 

# Filter df_add to include only new rows since the last processed date
df_add = df_add[df_add['DateTrans'] > last_cutoff_date]

len_df_add = len(df_add)
if len_df_add > 0 :
    # BUT NOW AFTER HERE OUR ACTUAL LAST DATE IS the last in df_add
    last_cutoff_date = df_add['DateTrans'].max() # Update for df_add !!!!

    # Print updates
    print('\n|||>_updt.py_> > > Processing Portfolio UPDATES for up to :\n')
    print(f" Rows processed: {len(df_add)}\n\n")

    last_cutoff_date_str = 'AfterAllCEA' # NEEDS to always have the same name 

    # Placeholder for OPENING CASH EXCESS UPDTS
    filter_cash_excess_check = 0  # MEANS OPEN LOOP FOR UPDTS CASH EXCESS
    # #Correct the use of exec function
    with open(f"{name_updt_ledger_till_ce}.py", "r", encoding="utf-8") as file:
        code = file.read()
        exec(code)
    #print(df)
    input('>>>>>>>>>>>> DONE ')
###
###### EXPORT table dependency for 1_a_CASH
###