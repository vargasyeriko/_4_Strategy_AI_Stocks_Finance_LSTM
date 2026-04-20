# # START

# if __name__ == "__main__":
#     try:
#         # Execute _run_11.py in its own namespace
#         exec(open("_run_11.py").read(), {})
#     except Exception as e:
#         # Print error messages
#         print("Error in _run_11.py:", e)

#     try:
#         #print(name_updt_ledger_till_ce)
#         # Execute _run_12.py in its own namespace
#         exec(open("_run_13.py").read(), {}) # does not passes output
#         # exec(open("_run_12.py").read(), globals()) # it does passes 

#     except Exception as e:
#         # Print error messages
#         print("Error in _run_13.py:", e)


def: new_hist_entries():
    rsp_now = input('Did you make any changes in the previous month? <Enter:skip> <y:add_change>')
    if rsp_now == 'y':
        #
        df= pd.read_pickle(f'_1_tables/_df_0_init_UNITS.pkl')
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
        print("1. Add exchange stock \n\t\t\t *a) : stock to stock",
              "\n\t\t\t *b) : stock to cash\n\n2. Buy stock from Excess cash")
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    
        choice = input("\nEnter your choice (1 or 2): ")
    
        # EXCHANGE STOCK
        if choice == "1":
            #subprocess.run(['python',f"{direc}/_0_a1_PORTFOLIO_entry_updt_.py"], cwd=f'{direc}')
            exec(open(f"_0_a1_PORTFOLIO_entry_updt_.py",encoding="utf-8").read()) #paths
    
        # CASH ECSESS
        elif choice == "2":
            exec(open(f"_0_a2_PORTFOLIO_entry_updt_.py",encoding="utf-8").read()) 
        else:
            print("Invalid choice. Please enter 1 or 2.")
    else:
        print('No CHANGES made ... CNTD ... \n')