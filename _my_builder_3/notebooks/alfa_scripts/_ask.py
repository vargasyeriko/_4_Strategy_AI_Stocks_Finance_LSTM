from datetime import datetime
import pandas as pd

from _0_0_all_stocks_ import d_start_date,total_inv,formatted_date_time


rsp_now = input('Did you make any changes in the previous month? <Enter:skip> <y:add_change>')
if rsp_now == 'y':
    #

    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    print("1. Add exchange stock \n\t\t\t *a) : stock to stock",
          "\n\t\t\t *b) : stock to cash\n\n2. Buy stock from Excess cash")
    print(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")

    choice = input("\nEnter your choice (1 or 2): ")

    # EXCHANGE STOCK
    if choice == "1":
        exchange_type = 'stock_exchange'
        exec(open(f"_ask_stock_exchange.py",encoding="utf-8").read())
    elif choice == "2":
        exchange_type = 'cash_excess'
        exec(open(f"_ask_stock_cash_excess.py",encoding="utf-8").read())

    else:
        print("Invalid choice. Please enter 1 or 2.")
else:
    print('No CHANGES made ... CNTD ... \n')


# # UPTD
# if __name__ == "__main__":
#     try:
#         # Execute _run_11.py in its own namespace
#         exec(open("updt.py").read(), {})
#     except Exception as e:
#         # Print error messages
#         print("Error in _run_11.py:", e)

#     # try:
#     #     #print(name_updt_ledger_till_ce)
#     #     # Execute _run_12.py in its own namespace
#     #     exec(open("_run_13.py").read(), {}) # does not passes output
#     #     # exec(open("_run_12.py").read(), globals()) # it does passes 

#     # except Exception as e:
#     #     # Print error messages
#     #     print("Error in _run_13.py:", e)

# # PDF
