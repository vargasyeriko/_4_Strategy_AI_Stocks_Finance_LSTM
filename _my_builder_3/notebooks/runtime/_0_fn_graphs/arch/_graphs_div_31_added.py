import pandas as pd
import matplotlib.pyplot as plt

# Load the master dataframe
df_master = pd.read_pickle(f'_1_tables/{nme_df_master}.pkl')

# Filter dataframes based on 'm_period'
_df_0m = df_master[df_master['m_period'] == '0m']
_df_3m = df_master[df_master['m_period'] == '3m']
_df_6m = df_master[df_master['m_period'] == '6m']
_df_12m = df_master[df_master['m_period'] == '12m']

# Calculate total dividends for each period
div_total_0_6 = _df_0m['dividend_total'].sum() + _df_3m['dividend_total'].sum() + _df_6m['dividend_total'].sum()
div_total_6_12 = _df_6m['dividend_total'].sum() + _df_12m['dividend_total'].sum()

# Prepare data for plotting
periods = ['0-6 Months', '6-12 Months']
dividends = [div_total_0_6, div_total_6_12]

# Create bar plot
plt.figure(figsize=(10, 6))
plt.bar(periods, dividends, color=['blue', 'green'])
plt.xlabel('Period')
plt.ylabel('Total Dividends')
plt.title('Total Dividends Comparison Between 0-6 Months and 6-12 Months')
plt.show()

plt.savefig('_0_out/_G31_dividend_growth.png', dpi=300)