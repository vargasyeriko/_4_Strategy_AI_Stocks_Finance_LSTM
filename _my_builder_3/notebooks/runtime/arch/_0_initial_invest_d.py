######################################
import matplotlib.pyplot as plt


# Calculate the amount of investment per stock
investment_amounts = [initial_investment * p for p in portfolio_percentages]

# Create pie chart
fig, ax = plt.subplots()
ax.pie(portfolio_percentages, labels=portfolio_labels, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Add legend with amounts and percentages
legend_labels = [f'{label}: ${amount:.2f} ({p*100:.1f}%)' for label, amount, p in zip(portfolio_labels, investment_amounts, portfolio_percentages)]
ax.legend(legend_labels, title="Portfolio Breakdown", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

plt.title('Portfolio Breakdown by Investment')
plt.tight_layout()
plt.show()

# Portfoltio Breakdown 

import pandas as pd

# Create a DataFrame for the portfolio investments
portfolio_data = {
    'Symbol': portfolio_labels,
    'Percentage': portfolio_percentages,
    'Investment_Amount': investment_amounts,
    'trans_amount':transaction_amount
}

portfolio_df = pd.DataFrame(portfolio_data)
print('Portfolio Breakdown ::: Calculate initial investment in each asset ::: portfolio_df :: \n\n',portfolio_df)

#Initial Investment 
print(f"\n\nInitial Investment\t : {initial_investment}   ::: var_name = initial_investment ")


# Column to sum
column_name = 'Investment_Amount'

# Sum of the specified column
total_inv = portfolio_df[column_name].sum()

print(f"Total of all investments : {total_inv} ::: var_name = total_inv ")

# CASH AMOUNT
cash_amount = initial_investment - total_inv

print(f"Cash Balance \t\t : {cash_amount}  ::: var_name = cash_amount")

# CASH AMOUNT after Transaction costs 

cash_amount_cost_trans = cash_amount -sum(transaction_amount)

print(f"Cash Balance w Costs \t : {cash_amount_cost_trans}  ::: var_name = cash_amount_cost_trans ")

# cash amount Percentage 

# cash_bal_per = cash_amount/initial_investment

# print(f"Cash Perc \t\t : {cash_bal_per}  ::: var_name = cash_bal_per")

# 
