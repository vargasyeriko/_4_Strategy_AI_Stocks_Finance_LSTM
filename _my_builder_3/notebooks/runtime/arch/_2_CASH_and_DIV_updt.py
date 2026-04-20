
### CASH BAL
# cash % INIT
cash_start_value = cash_start_value_d+cash_start_value_g
#
print('\n\n************************DIV & CASH****************************** ')

print('cash_start_value\t\t\t',cash_start_value,'\ntrans_cost_all_but_cash_stock_buys\t',
trans_cost_all_but_cash_stock_buys)

import pandas as pd

# Assuming df_cash is your existing DataFrame and it has the columns 'Amount Bought_no_tf' and 'DateTrans'

# Create a new DataFrame df_cash_bal with selected columns and rename 'Amount Bought_no_tf' to 'amount'
df_cash_bal = df_cash[['Amount Bought_no_tf', 'DateTrans']].copy()
df_cash_bal.rename(columns={'Amount Bought_no_tf': 'amount'}, inplace=True)
df_cash_bal['id_time_buy'] = df_cash['id_time_buy'].copy()
df_cash_bal['trans_type'] = 'stock_to_cash'

if 'costs' not in df_cash.columns:
    # If not, add 'costs' column with all values set to 0
    df_cash_bal['costs'] = 0
    
# Your df_cash_bal now contains the 'amount' and 'DateTrans' columns
#df_cash_bal
# CASH INIT

# Create a new row to append to df_cash_bal
new_row = {
    'amount': cash_start_value,  # Adding cash_start_value to amount
    'DateTrans': d_start_date,  # Setting DateTrans to d_start_date
    'id_time_buy': f'Def_init_INV_{d_start_date}',  # Setting id to 'Def_init_INV_{d_start_date}'
    'trans_type': 'cash_init',  # Setting transaction type to 'cash_init'
    'costs': 0  # Setting costs to 0
}

# Append the new row to df_cash_bal
df_cash_bal = df_cash_bal.append(new_row, ignore_index=True)
# TRANS COSTS

# Create a new row to append to df_cash_bal
new_row = {
    'amount': 0,  # Adding cash_start_value to amount
    'DateTrans':'start-end' , # Setting DateTrans to d_start_date
    'id_time_buy': 'id_trans_cost_1' , # Setting id to 'Def_init_INV_{d_start_date}'
    'trans_type': 'trans_cost_all_but_cash_stock_buys',  # Setting transaction type to 'cash_init'
    'costs': trans_cost_all_but_cash_stock_buys  # Setting costs to 0
}

# Append the new row to df_cash_bal
df_cash_bal = df_cash_bal.append(new_row, ignore_index=True)
df_cash_bal

########################################################## ADD CASH BALANCE TABLE ####

import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_stock_price_on_date(stock_symbol, date):
    """
    Fetches the closing price of a stock on a specific date using yfinance.
    Expands the search range to accommodate for weekends and holidays.
    """
    try:
        start_date = (datetime.strptime(date, "%Y-%m-%d") - pd.Timedelta(days=2)).strftime("%Y-%m-%d")
        end_date = (datetime.strptime(date, "%Y-%m-%d") + pd.Timedelta(days=2)).strftime("%Y-%m-%d")
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
        
        if not stock_data.empty:
            if date in stock_data.index.strftime("%Y-%m-%d").tolist():
                return stock_data.loc[date]['Close']
            else:
                return stock_data['Close'].iloc[0]
    except Exception as e:
        print(f"Error fetching data for {stock_symbol} on {date}: {e}")
    return None

def calculate_units_with_transaction_fee(df):
    """
    Calculates the number of units that can be bought for each stock listed in the DataFrame,
    accounting for transaction fees.
    """
    df['DateTrans'] = pd.to_datetime(df['DateTrans']).dt.strftime('%Y-%m-%d')
    df['buying_power'] = df['CASH'] * (df['Percent_buy'] / 100)
    
    # Calculate transaction fees
    transaction_fees = []
    for index, row in df.iterrows():
        amount = row['buying_power']
        if amount > 7334:
            fee = amount * 0.0009
        elif amount == 0.0:
            fee = 0.0
        else:
            fee = 6.60
        transaction_fees.append(fee)
    
    df['transaction_fee'] = transaction_fees
    df['cash_exchange'] = df['buying_power'] - df['transaction_fee']
    
    units_can_buy = []
    for index, row in df.iterrows():
        stock = row['Stock']
        date_trans = row['DateTrans']
        cash_exchange = row['cash_exchange']
        
        closing_price = fetch_stock_price_on_date(stock, date_trans)
        
        if closing_price:
            units = cash_exchange / closing_price
        else:
            units = 0
            print(f"No price data available for {stock} on {date_trans}")
        
        units_can_buy.append(units)
    
    df['units_updts'] = units_can_buy
    return df


