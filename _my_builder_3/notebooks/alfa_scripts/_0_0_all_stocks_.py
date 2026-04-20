from datetime import datetime

import pandas as pd
from _fns import concat_pkl_to_df 
### #########################
### #########################
### ######################### INIT
    ## Initial Investment & START DATE
d_start_date = '2022-07-01'
total_inv = 100000 
start_date_reset = d_start_date

now = datetime.now();formatted_date_time = now.strftime("%Y_%m_%d_h%Hm%M")
### ########################################################################## CE
stock_list_ce = ['BUGG.AX']

df_ce_start= pd.DataFrame({
        'date_cash_to_stock': ['2024-02-15'],
        'per_cash_to_stock': [30 ],
        'Stock': stock_list_ce
    })
df_ce_all_hist = concat_pkl_to_df(df_ce_start, directory="_12_tables_ce/")

stock_list_ce = df_ce_all_hist['Stock'].tolist()
### ########################################################################## G
### Initial Stocks 
portfolio_labels_d = ['DHOF.AX', 'ILB.AX', 'QPON.AX', 'TACT.XA', 'GROW.AX', 
                    'MVA.AX', 'GOLD.AX']
## PERCENTAGES
portfolio_percentages_d = [0.141, 0.1866, 0.1866, 0.1766, 0.069, 0.1, 0.08] #million 

# The data to append as a DataFrame, now excluding 'AmountSold' and 'AmountBought' # history of sells
data_to_append_df_d = pd.DataFrame([
    {'Stock': 'TACT.XA', 'PercentSold': 25.0, 'keep_drop': 'd', 'trans_type': 's',
     'DateTrans': '2023-05-03','exchange_stocks': ['ILB.AX'] ,'sell_perc': [100]},
    
    {'Stock': 'GOLD.AX', 'PercentSold': 66.0, 'keep_drop': 'd', 'trans_type': 's', 
     'DateTrans': '2023-07-20','exchange_stocks':['QPON.AX']  ,'sell_perc': [100]}, 
    # updt sell %66
    
    {'Stock': 'MVA.AX', 'PercentSold': 100.0, 'keep_drop': 'd', 'trans_type': 's', 
     'DateTrans': '2023-09-11','exchange_stocks': ['QPON.AX', 'ILB.AX']  ,'sell_perc': [50, 50]},
    
    {'Stock': 'QPON.AX', 'PercentSold': 23.0, 'keep_drop': 'd', 'trans_type': 's', 
     'DateTrans': '2024-02-13','exchange_stocks':['HCRD.AX', 'USIG.AX']  ,'sell_perc': [35, 65]},
    
    {'Stock': 'ILB.AX', 'PercentSold': 35.0, 'keep_drop': 'd', 'trans_type': 's', 
     'DateTrans': '2024-02-13','exchange_stocks':['HCRD.AX', 'USIG.AX']  ,'sell_perc': [50, 50]},
    
    
    {'Stock': 'DHOF.AX', 'PercentSold': 50.0, 'keep_drop': 'd', 'trans_type': 's', 
     'DateTrans': '2024-02-13','exchange_stocks':['HCRD.AX']  ,'sell_perc': [100]},
    

])
### ########################################################################## G
### Initial Stocks 
portfolio_labels_g = ['AMC.AX', 'ALD.AX', 'ANZ.AX', 'APA.AX', 'BHP.AX','SQ2.AX', 'BXB.AX', 'CHC.AX', 'COL.AX', 'CBA.AX', 
                    'CSL.AX', 'CSR.AX', 'IAG.AX', 'JLG.AX', '360.AX',
                    'PXA.AX', 'RHC.AX', 'RMD.AX', 'SHL.AX', 'TLS.AX', 
                    'TCL.AX', 'EX20.AX', 'WES.AX', 'VCX.AX', 'XRO.AX',
                    'QUAL.AX', 'ANN.AX', 'GLOB.AX', 'FEMX.AX', 'MCSI.XA',
                    'CLDD.AX','DJRE.AX', 'ACDC.AX']

## PERCENTAGES
portfolio_percentages_g =[ .0311, .0142, .0255, .011, .0255, .0089, .0127, .0283, .0177, .025, 
                        .032, .0099, .0085, .0095, .0144, .022, .0105, .0144, .012, .0142,
                        .01, .0442, .0211, .0111, .0111, .1177, .0305, .1177, .101, .0408, .03684,.048, .062]


# The data to append as a DataFrame, now excluding 'AmountSold' and 'AmountBought' # history of sells
data_to_append_df_g = pd.DataFrame([
    {'Stock': 'SQ2.AX', 'PercentSold': 30.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2022-10-27','exchange_stocks': ['RHC.AX'] ,'sell_perc': [100]},
    {'Stock': 'CBA.AX', 'PercentSold': 25.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2022-12-01','exchange_stocks':['IAG.AX']  ,'sell_perc': [100]},
    {'Stock': 'BHP.AX', 'PercentSold': 19.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-03-10','exchange_stocks': ['TCL.AX']  ,'sell_perc': [100]}, 
    {'Stock': 'BXB.AX', 'PercentSold': 15.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-03-10','exchange_stocks':['TCL.AX']  ,'sell_perc': [100]},
    {'Stock': 'JLG.AX', 'PercentSold': 15.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-03-10','exchange_stocks':['TCL.AX']  ,'sell_perc': [100]},

    {'Stock': 'EX20.AX', 'PercentSold': 50.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-03-13','exchange_stocks':['VHY.AX']  ,'sell_perc': [100]},
    {'Stock': 'QUAL.AX', 'PercentSold': 30.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-03-10','exchange_stocks':['FEMX.AX']  ,'sell_perc': [100]},
    {'Stock': 'CSL.AX', 'PercentSold': 38.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-07-20','exchange_stocks':['SHL.AX']  ,'sell_perc': [100]},  
    {'Stock': 'DJRE.AX', 'PercentSold': 100.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-07-20','exchange_stocks':['IJH.AX', 'ANZ.AX']  ,'sell_perc': [50, 50]},
    {'Stock': 'ACDC.AX', 'PercentSold': 100.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-07-20','exchange_stocks':['TSLA']  ,'sell_perc': [100]},
    
    {'Stock': 'FEMX.AX', 'PercentSold': 50.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-09-11','exchange_stocks':['TLS.AX', 'CSR.AX']  ,'sell_perc': [33, 67]},
   
    {'Stock': 'CLDD.AX', 'PercentSold': 15.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-10-10','exchange_stocks':['CASH','TSLA']  ,'sell_perc': [70, 30]},
    {'Stock': 'QUAL.AX', 'PercentSold': 15.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2023-10-10','exchange_stocks':['CASH','TSLA']  ,'sell_perc': [70, 30]},

    {'Stock': 'ANN.AX', 'PercentSold': 100.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2024-01-10','exchange_stocks':['RMD.AX']  ,'sell_perc': [100]},

    {'Stock': 'PXA.AX', 'PercentSold': 100.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2024-02-13','exchange_stocks':['MQG.AX']  ,'sell_perc': [100]},
    {'Stock': 'VCX.AX', 'PercentSold': 100.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2024-02-13','exchange_stocks':['MIN.AX']  ,'sell_perc': [100]},

    {'Stock': 'CLDD.AX', 'PercentSold': 100.0, 'keep_drop': 'd', 'trans_type': 's', 'DateTrans': '2024-02-13','exchange_stocks':['SEMI.AX']  ,'sell_perc': [100]},


])

##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################
##########################################################################


