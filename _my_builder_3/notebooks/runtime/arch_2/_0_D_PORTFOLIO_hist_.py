# def _PORT_DEF_get():

#     ### ############################################################################
#     #print('\n -> DEFENSIVE')
#     ### Start Dates -> they are 9 because of cash and trans_cost
#     len_stocks_d = len(portfolio_labels_d)
#     start_date = [d_start_date] * (len_stocks_d+2)
    
#     ### Initial investments and portfolio setup
#     portfolio_percentages = portfolio_percentages_d
    
#     #print(portfolio_percentages)
#     ############################################################################data_to_append_df_d
#     df_columns = ['Stock', 'PercentSold', 'keep_drop', 'trans_type', 'DateTrans','exchange_stocks','sell_perc']
#     hist_df_d = pd.DataFrame(columns=df_columns)  # Initialize with the updated columns
    
    
#     hist_df_d = pd.concat([hist_df_d, data_to_append_df_d], ignore_index=True)
    
#     # Ensure that all entries in 'exchange_stocks' and 'sell_perc' are lists of strings
#     hist_df_d['exchange_stocks'] = hist_df_d['exchange_stocks'].apply(lambda lst: [str(item) for item in lst])
#     hist_df_d['sell_perc'] = hist_df_d['sell_perc'].apply(lambda lst: [str(percentage) for percentage in lst])
#     hist_df_d['id_time'] = hist_df_d['Stock'] + "_" + hist_df_d['DateTrans'] + "_" + hist_df_d['trans_type']
    
#     initial_investment = initial_investment_D  # AUD
#     #
#     #print(f'\nInitial Investment is {initial_investment}')
#     # Calculate the total percentage currently allocated to stocks
#     total_percentage_allocated = sum(portfolio_percentages)
#     cash_percentage = 1 - total_percentage_allocated  # Remaining percentage for cash
    
#     # Update the portfolio to include cash
#     portfolio_percentages.append(cash_percentage)
#     portfolio_labels_d.append('Cash')
    
#     # Calculate invested amounts including the cash component
#     invested_amounts = [percentage * initial_investment for percentage in portfolio_percentages]
    
#     # Determine the transaction fee, assuming no fee for cash
#     transaction_fees = []
#     for amount in invested_amounts[:-1]:  # Exclude cash for fee calculation
#         if amount > 7334:
#             fee = amount * 0.0009
#         if amount == 0.0:
#             fee = 0.0
#         else:
#             fee = 6.60
#         transaction_fees.append(fee)
#     transaction_fees.append(0)  # No fee for cash
    
#     # Calculate net cash value after fees for all components including cash
#     net_cash_values = [amount - fee for amount, fee in zip(invested_amounts, transaction_fees)]
    
#     # Create a DataFrame to display the portfolio with cash values
#     portfolio_df = pd.DataFrame({
#         'Stock': portfolio_labels_d,
#         'Invested Amount (AUD)': invested_amounts,
#         'Transaction Fee (AUD)': transaction_fees,
#         'Net Cash Value (AUD)': net_cash_values
#     })
#     # Calculate totals and sums for transactions
#     total_sum_inv = portfolio_df['Invested Amount (AUD)'].sum()
#     entry_sum_trans = portfolio_df['Transaction Fee (AUD)'].sum()
#     entry_inv_from_trans = 0
#     net_trans_cost = 0 + entry_sum_trans
    
#     # Assign transaction cost summary
#     # New row values
#     new_row_values = ['trans_cost', entry_inv_from_trans, entry_sum_trans, net_trans_cost]
    
#     # Adding new row using loc
#     portfolio_df.loc[len(portfolio_df)] = new_row_values
    
#     # Assign Start Date to each row
#     portfolio_df['StartDate'] = start_date
    
#     # Convert StartDate column to a list
#     start_dates_list_d = portfolio_df['StartDate'].tolist()
    
#     ############
    
#     # Calculate the percentages for the legend
#     portfolio_df['Percentage'] = (portfolio_df['Net Cash Value (AUD)'] / portfolio_df['Net Cash Value (AUD)'].sum()) * 100
    
#     df_cash_start_d = portfolio_df.tail(2)
#     cash_start_value_d = portfolio_df.loc[portfolio_df['Stock'] == 'Cash', 'Invested Amount (AUD)'].values[0]
    
#     ##################
    
#     # Getting the first column excluding the last two rows
#     stock_names_d = portfolio_df.iloc[:-2, 0].tolist()
#     stock_net_start_d = portfolio_df.iloc[:-2, 3].tolist()
    
#     # Assuming df_close is already loaded and prepared
#     investment_details = []
    
#     # Iterate over stocks and their corresponding start dates
#     for stock_symbol, start_date in zip(stock_names_d, start_dates_list_d):
#         results = calculate_investment_details([start_date], stock_symbol, df_close)
#         for start_price, latest_price in results:
#             investment_details.append({
#                 "Stock": stock_symbol,
#                 "Price Bought": start_price,
#                 "Latest Price": latest_price
#             })
    
#     # Convert investment details to DataFrame
#     investment_df_d = pd.DataFrame(investment_details)
    
#     # Merging with the original portfolio DataFrame
#     df_d = pd.merge(investment_df_d, portfolio_df, on='Stock', how='outer')
#     df_d['hold_units_at_init'] = df_d['Net Cash Value (AUD)'] / df_d['Price Bought']
    
    
#     ##### HIST 
#     return hist_df_d,df_d,cash_start_value_d
    
