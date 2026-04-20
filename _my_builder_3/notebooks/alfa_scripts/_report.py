exec(open(f"_22_tbls.py",encoding="utf-8").read())

df = df_report.copy()

brokerage_paid = df['trans_fee'].sum()
initial_investment= 100000 
d_start_date= '2022-07-01'
cash_init = 1852.200000
# Monthly returns table 
df = df.drop_duplicates(subset=['period'], keep='first')
df = df[['AnalysisEndDate','period',
       'period_divs','period_total_cash',
       'period_stocks_value','period_total_holds'
      ]]

per_inv = len(df)
new_row = {
    "AnalysisEndDate": d_start_date,
    "period": per_inv,  # Assigning -1 to denote initial state before period 0

    "period_divs": 0,
    "period_total_cash": cash_init+0,
    "period_stocks_value": initial_investment-cash_init,
    "period_total_holds": initial_investment
}

# Appending the new row
df = df.append(new_row, ignore_index=True)
df.sort_values(by='period', ascending=True, inplace=True)
# Calculate monthly returns
df = df.merge(df_br_costs, on='period', how='left').copy()
# ACCOUNT NOW FOR TRANS FEES.

df['cash_shifted_last'] = df['period_total_cash'].shift(-1)
df['stock_shifted_last'] = df['period_stocks_value'].shift(-1)

df_1cp = df.copy()

all_trans_fee = df_1cp['trans_fee'].sum()

# RESET
df1r = df_1cp.copy()
df_1cp = df1r.copy()


# Calculate the change in CASH FLOW values between the current period and the next period

df_1cp['period_DIFF_cash'] = df_1cp['period_total_cash']-df_1cp['cash_shifted_last']
# Calculate the change in stock values between the current period and the next period
df_1cp['period_DIFF_stock'] = df_1cp['period_stocks_value'] - df_1cp['stock_shifted_last']

df_1cp['return_percentage'] = ((df_1cp['period_stocks_value'] - df_1cp['stock_shifted_last'] + df_1cp['period_DIFF_cash']) / df_1cp['stock_shifted_last']) * 100


df_1cp['total_return'] = ((df_1cp['period_total_holds']/initial_investment)-1)*100




############################# MSG 1
# Convert 'AnalysisEndDate' to datetime just once for the whole DataFrame
df_1cp['AnalysisEndDate'] = pd.to_datetime(df_1cp['AnalysisEndDate'])

# Get the first and last date from the DataFrame
start_date = df_1cp.iloc[-1]['AnalysisEndDate']
end_date = df_1cp.iloc[0]['AnalysisEndDate']
# Extract the day of the month for both start and end dates
start_day = start_date.day
end_day = end_date.day
# Format these dates to extract month and year
start_month = start_date.strftime('%B %Y')
end_month = end_date.strftime('%B %Y')


end_date = df_1cp.iloc[0]['AnalysisEndDate']
m_ret = df_1cp.iloc[0]['return_percentage']
#print(f'{end_date}')
message_mr = f"""The total monthly percentage return of the fund including 
monthly dividends to end date of {end_date.strftime('%d %B %Y')}, was: {m_ret:.2f}%
"""
#print(message_mr)

############################# MSG 1
# Convert 'AnalysisEndDate' to datetime just once for the whole DataFrame
df_1cp['AnalysisEndDate'] = pd.to_datetime(df_1cp['AnalysisEndDate'])

# Get the first and last date from the DataFrame
start_date = df_1cp.iloc[-1]['AnalysisEndDate']
end_date = df_1cp.iloc[0]['AnalysisEndDate']
# Extract the day of the month for both start and end dates
start_day = start_date.day
end_day = end_date.day
# Format these dates to extract month and year
start_month = start_date.strftime('%B %Y')
end_month = end_date.strftime('%B %Y')


end_date = df_1cp.iloc[0]['AnalysisEndDate']
m_ret = df_1cp.iloc[0]['return_percentage']
#print(f'{end_date}')
message_mr = f"""The total monthly percentage return of the fund including 
monthly dividends to end date of {end_date.strftime('%d %B %Y')}, was: {m_ret:.2f}%
"""
#print(message_mr)



############################# MSG 1

# Convert 'AnalysisEndDate' to datetime just once for the whole DataFrame
#df_1cp['AnalysisEndDate'] = pd.to_datetime(df_1cp['AnalysisEndDate'])

# Get the first and last date from the DataFrame
start_date = df_1cp.iloc[-1]['AnalysisEndDate']
end_date = df_1cp.iloc[0]['AnalysisEndDate']
# Extract the day of the month for both start and end dates
start_day = start_date.day
end_day = end_date.day
# Format these dates to extract month and year
start_month = start_date.strftime('%B %Y')
end_month = end_date.strftime('%B %Y')


total_return = df_1cp.iloc[0]['total_return'] # here is logical that you use the last full amount 

message_tr = f"""The total return of the fund including dividends and,
cash flow since Inception the end date of {end_date.strftime('%d %B %Y')}, was:  {total_return:.2f}%
"""
#print(message_tr)
############################# MSG 1

# Convert 'AnalysisEndDate' to datetime just once for the whole DataFrame
df_1cp['AnalysisEndDate'] = pd.to_datetime(df_1cp['AnalysisEndDate'])

# Get the first and last date from the DataFrame
start_date = df_1cp.iloc[-1]['AnalysisEndDate']
end_date = df_1cp.iloc[0]['AnalysisEndDate']
# Extract the day of the month for both start and end dates
start_day = start_date.day
end_day = end_date.day
# Format these dates to extract month and year
start_month = start_date.strftime('%B %Y')
end_month = end_date.strftime('%B %Y')

# Get the return percentage from the first recordable calculation
total_return_stocks = df_1cp.iloc[0]['period_stocks_value']  # This picks the latest month's return
# Create the message
message_psr = f"""The total Stock Holding Value at the end date of {end_date.strftime('%d %B %Y')}, was: {total_return_stocks:.2f} $
"""
#print(message_psr)

############################# MSG 1
# Convert 'AnalysisEndDate' to datetime just once for the whole DataFrame
df_1cp['AnalysisEndDate'] = pd.to_datetime(df_1cp['AnalysisEndDate'])

# Get the first and last date from the DataFrame
start_date = df_1cp.iloc[-1]['AnalysisEndDate']
end_date = df_1cp.iloc[0]['AnalysisEndDate']
# Extract the day of the month for both start and end dates
start_day = start_date.day
end_day = end_date.day
# Format these dates to extract month and year
start_month = start_date.strftime('%B %Y')
end_month = end_date.strftime('%B %Y')

# divs
total_return_divs = df_1cp.iloc[0]['period_divs']

# Create the message
message_pca = f"""
The total Dividends amount from {start_date.strftime('%d %B %Y')} to {end_date.strftime('%d %B %Y')}, was: {total_return_divs:.2f} $
"""
#print(message_pca)


############################# MSG 1
# Convert 'AnalysisEndDate' to datetime just once for the whole DataFrame
df_1cp['AnalysisEndDate'] = pd.to_datetime(df_1cp['AnalysisEndDate'])

# Get the first and last date from the DataFrame
start_date = df_1cp.iloc[1]['AnalysisEndDate']
end_date = df_1cp.iloc[0]['AnalysisEndDate']
# Extract the day of the month for both start and end dates
start_day = start_date.day
end_day = end_date.day
# Format these dates to extract month and year
start_month = start_date.strftime('%B %Y')
end_month = end_date.strftime('%B %Y')

# divs
total_return_divs = (df_1cp.iloc[0]['period_divs'] - df_1cp.iloc[1]['period_divs'])/df_1cp.iloc[1]['period_divs']

# Create the message
message_psd = f"""The total monthly Dividends yield from  {start_date.strftime('%d %B %Y')} to {end_date.strftime('%d %B %Y')}, was: {total_return_divs:.2f} $
"""
#print(message_psd)


############################# MSG 1


# current cash excess amount 

# Get the first and last date from the DataFrame
start_date = df_1cp.iloc[-1]['AnalysisEndDate']
end_date = df_1cp.iloc[0]['AnalysisEndDate']


# Since start_date and end_date are already datetime objects, you can directly use them
# Extract the day of the month for both start and end dates
start_day = start_date.day
end_day = end_date.day

# Format these dates to extract month and year
start_month = start_date.strftime('%B %Y')
end_month = end_date.strftime('%B %Y')

# Get the return percentage from the first recordable calculation
total_return =  df_1cp.iloc[0]['period_total_cash']  # This picks the latest month's return

message_pcb = f'The current cash in this portfolio including dividends is {total_return}'



############################# MSG 1


# YEARLY yield and that it 


# Get the first and last date from the DataFrame
start_date = df_1cp.iloc[-1]['AnalysisEndDate']
end_date = df_1cp.iloc[0]['AnalysisEndDate']

# Since start_date and end_date are already datetime objects, you can directly use them
# Extract the day of the month for both start and end dates
start_day = start_date.day
end_day = end_date.day

# Format these dates to extract month and year
start_month = start_date.strftime('%B %Y')
end_month = end_date.strftime('%B %Y')
# Get the first and last date from the DataFrame


final_value = total_return_stocks
dividends_received = total_return_divs

total_adjusted_final = final_value - initial_investment + dividends_received - all_trans_fee
time_difference = (end_date - start_date).days / 365.25  # Use 365.25 to account for leap years

CAGR = ((final_value + dividends_received - all_trans_fee) / initial_investment) ** (1 / time_difference) - 1
CAGR_percentage = CAGR * 100

message_cagr =f"""
The Compound Annual Growth Rate (CAGR) for the portfolio
from {start_date.strftime('%d %B %Y')} to {end_date.strftime('%d %B %Y')} is approximately {CAGR_percentage:.2f}% per annum
"""

#print(message_cagr)



######################################################
###############################################################
report_p1 = f"""
*********************************************************************

Assuming Balance Growth, we have the following:

Portfolio Initial investment is: ${initial_investment} 
Approximately, we have blockage costs of: ${all_trans_fee}

{message_mr}
{message_tr}
{message_psr}
 -{message_psd}
 -{message_pcb}
{message_pca}
{message_cagr}
*********************************************************************
"""
def report_p1_fn(report_p1):
    print(report_p1)
    return report_p1
print(report_p1)


######################################################
############################################################### DF organization 

df_1cp_1 = df_1cp[['AnalysisEndDate','return_percentage','period_total_holds','period']]

# Define the specific values for the columns you want to update
new_values = {
    'return_percentage': 0}

# Make a copy of the DataFrame to avoid SettingWithCopyWarning
df_1cp_1 = df_1cp_1.copy()
# Replace the specified columns in the last row with the new values using .loc
for col, value in new_values.items():
    df_1cp_1.loc[df_1cp_1.index[-1], col] = value

df_from_scratch =df_1cp_1.copy()

df_from_scratch['period'] = df_1cp_1['period'][::-1].reset_index(drop=True).copy()

df_from_scratch.sort_values(by='AnalysisEndDate', ascending=False, inplace=True)
df_from_scratch['AnalysisEndDate'] = pd.to_datetime(df_from_scratch['AnalysisEndDate'])
df_from_scratch 



######################################################
###############################################################
# Returns Graph
######################################################
###############################################################

#print(report_p1)

# Recalculate percentage increase since the first investment day (period 22)
initial_value = df_from_scratch['period_total_holds'].iloc[-1]  # Get the value for period 22
df_from_scratch['percentage_increase'] = ((df_from_scratch['period_total_holds'] - initial_value) / initial_value) * 100

# Recreate the graph with corrected x-axis labels and percentage increase calculations
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 20), gridspec_kw={'height_ratios': [4, 1]}, dpi=300)

# Graph
ax1.plot(df_from_scratch['AnalysisEndDate'], df_from_scratch['period_total_holds'], marker='o', markersize=6, linestyle='-', linewidth=2.5, color='darkblue')
ax1.axhline(y=initial_value, color='gray', linestyle='--', linewidth=3, label=f'Initial Value: ${initial_value:,.2f}')
ax1.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m'))
ax1.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=2))
ax1.set_xlabel('Date', fontsize=16)
ax1.set_ylabel('Total Holdings ($)', fontsize=16)
ax1.set_title('Returns Graph Starting from the Earliest Period', fontsize=19)
ax1.legend()
ax1.grid(True, linestyle='--', linewidth=0.9, alpha=0.2)

# Table
cell_text = []
cell_colors = []
for i, row in df_from_scratch.iterrows():
    cell_text.append([row['AnalysisEndDate'].strftime('%Y-%m-%d'), f"{row['percentage_increase']:.2f}%"])
    cell_colors.append(['w', 'w'])  # Background color for each cell
columns = ['Date', 'Percentage Increase']

# Adding a table at the bottom of the axes
table = ax2.table(cellText=cell_text, colLabels=columns, loc='center', cellLoc='center', colColours=['#dddddd']*2,
                  cellColours=cell_colors, fontsize=14)
ax2.axis('off')  # Hide the axes
table.auto_set_font_size(False)
table.set_fontsize(14)  # Set font size
table.scale(0.5, 2.9)  # Scale table (1 in x, 1.5 in y for row height)

# Adjust layout to accommodate both graph and table
plt.tight_layout()
plt.subplots_adjust(bottom=0.24)  # Adjust bottom margin to make room for x-axis labels
plt.savefig('_PY_ultimate_Final_Returns_Graph.png')
plt.show()








######################################################
###############################################################
# Returns Table 
######################################################
###############################################################

import pandas as pd

# Assuming df_from_scratch is your DataFrame and it is already loaded

# Convert 'AnalysisEndDate' to datetime
df_from_scratch['AnalysisEndDate'] = pd.to_datetime(df_from_scratch['AnalysisEndDate'])

# Sort DataFrame by 'AnalysisEndDate'
df_from_scratch = df_from_scratch.sort_values(by='AnalysisEndDate')

# Set 'AnalysisEndDate' as the index
df_from_scratch.set_index('AnalysisEndDate', inplace=True)

# Function to calculate rolling returns
def calculate_rolling_return(df, window):
    if len(df) >= window:
        return (df['return_percentage'].rolling(window=window).apply(lambda x: (1 + x / 100).prod() - 1) * 100).iloc[-1]
    return None

# Calculate rolling returns
one_month_return = calculate_rolling_return(df_from_scratch, 1)
three_month_return = calculate_rolling_return(df_from_scratch, 3)
six_month_return = calculate_rolling_return(df_from_scratch, 6)
one_year_return = calculate_rolling_return(df_from_scratch, 12)
two_year_return = calculate_rolling_return(df_from_scratch, 24)
three_year_return = calculate_rolling_return(df_from_scratch, 36)

# Calculate since inception return from the first date to the latest available date using compound returns
since_inception_return = (df_from_scratch['return_percentage'].apply(lambda x: 1 + x / 100).prod() - 1) * 100

# Get the latest returns
latest_data = {
    "1 Month Return": one_month_return,
    "3 Month Return": three_month_return,
    "6 Month Return": six_month_return,
    "1 Year Return": one_year_return,
    "2 Year Return": two_year_return,
    "3 Year Return": three_year_return,
    "Since Inception Return": since_inception_return
}

# Print the results
for period, value in latest_data.items():
    if value is not None:
        print(f"{period}: {value:.2f}%")
    else:
        print(f"{period}: -")


benchmark = {
    '1 Month Return': -2.3781462517712252,
    '3 Month Return': 4.455184823426515,
    '6 Month Return': 15.567881997712469383,
    '1 Year Return': 9.450968385650105,
    '2 Year Return': None,
    '3 Year Return': None,
    'Since Inception Return': 19.8921644474062677
}





######################################################
###############################################################
# Returns Graph
######################################################
###############################################################
import pandas as pd
import matplotlib.pyplot as plt



# Create DataFrame
data = {
    '1m': [latest_data['1 Month Return'], benchmark['1 Month Return']],
    '3m': [latest_data['3 Month Return'], benchmark['3 Month Return']],
    '6m': [latest_data['6 Month Return'], benchmark['6 Month Return']],
    '1y': [latest_data['1 Year Return'], benchmark['1 Year Return']],
    '2y': [latest_data['2 Year Return'], benchmark['2 Year Return']],
    '3y': [latest_data['3 Year Return'], benchmark['3 Year Return']],
    'Inception': [latest_data['Since Inception Return'], benchmark['Since Inception Return']]
}

# Convert to DataFrame and calculate the difference row
df = pd.DataFrame(data, index=['Portfolio', 'Benchmark'])
df.loc['Difference'] = df.loc['Portfolio'] - df.loc['Benchmark']

# Replace None with '-' and round to 2 decimal places
df = df.applymap(lambda x: '-' if pd.isna(x) else round(x, 2))

# Plotting
fig, ax = plt.subplots(figsize=(14, 10))
ax.axis('tight')
ax.axis('off')

# Create the table
table = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, cellLoc='center', loc='center')

# Style adjustments
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.7, 1.5)

# Enhance table appearance
for key, cell in table.get_celld().items():
    cell.set_edgecolor('black')
    cell.set_linewidth(1.5)
    if key[0] == 0:  # Header row
        cell.set_facecolor('#40466e')
        cell.set_text_props(color='white', weight='bold')
    if key[1] == -1:  # Row labels
        cell.set_facecolor('#40466e')
        cell.set_text_props(color='white', weight='bold')

# Set alternating row colors for better readability
rows, cols = df.shape
for row in range(1, rows + 1):
    for col in range(cols):
        cell = table[row, col]
        if row % 2 == 0:
            cell.set_facecolor('#f1f1f1')
        else:
            cell.set_facecolor('white')

# Adjust layout to make sure everything fits
plt.tight_layout()

# Save the plot with bbox_inches='tight' to ensure no clipping
plt.savefig('_PY_Compound_Returns.png', bbox_inches='tight', dpi=300)
plt.show()








######################################################
###############################################################
# Returns Graph
######################################################
###############################################################








































































