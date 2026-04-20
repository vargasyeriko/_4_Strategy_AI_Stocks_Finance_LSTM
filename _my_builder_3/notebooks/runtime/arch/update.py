# ############################################################################
# ############################################################################
# # ASK if there are updates last month
# rsp_now = input('Did you make any changes in the previous month? ') 
# #
# if rsp_now == 'y':
#     exec(open(f"_0_a_PORTFOLIO_entry_updt_.py",encoding="utf-8").read()) #paths
# else:
#     print('No CHANGES made ... CNTD ... \n')
# #START
# ############################################################################
# #_0_## PORTFOLIO UPDATES _ EXCHANGES _
# exec(open(f"_0_PORTFOLIO_updt_.py",encoding="utf-8").read()) #paths
# # ############################################################################
# #_1_## PORTFOLIO UPDATES _CASH_ DIVIDENS _
# # ############################################################################
# exec(open(f"_1_CASH_and_DIV_updt.py",encoding="utf-8").read())
# # #############################
# # #_1_a_ BUY FROM CASH
# exec(open(f"_1_a_CASH_Excess_.py",encoding="utf-8").read()) #paths
# # ############################################################################
# # ############################################################################
# # ################################# *************** ***************** *************** NEEDS asking fn CASH
# # import pandas as pd
# data = {
#     'date_cash_to_stock': ['2024-02-13'] ,
#     'per_cash_to_stock': [30] ,
#     'stock_from_cash': ['BUGG.AX'] }

# df_cash_x_stock_ads = pd.DataFrame(data).sort_values(by='date_cash_to_stock');df_cash_x_stock_ads
# # Sum to break loop
# filter_cash_excess = df_cash_x_stock_ads['per_cash_to_stock'].sum()
# # ################################# *************** ***************** *************** NEEDS asking fn CASH
# # ############################################################################
# # ############################################################################
# # ###_1_b_ 
# exec(open(f"_1_b_CASH_Excess_updt.py",encoding="utf-8").read()) #paths
# # ############################################################################
# # print(len(_df_0m),'\n Exporting updt DF for future buys/sells ::_2_up_to_date_df0m_.pkl::\n','\n')
# # _df_0m.to_pickle(f'_1_tables/_2_up_to_date_df0m_.pkl')
# # # print('
# # #df_master.to_pickle(f'tables/_3_up_to_date_DIVIDENDS.pkl');print('df_master exported to ::: tables/_3_up_to_date_DIVIDENDS.pkl')
# # #_2_## GRAPHS
# # ############################################################################
# # ############################################################################
# # #exec(open(f"_2_.py",encoding="utf-8").read())
# # ############################################################################
# # ############################################################################


