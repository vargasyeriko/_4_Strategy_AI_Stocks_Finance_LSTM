import matplotlib.pyplot as plt
import pandas as pd

# Assuming df_master is predefined and loaded with your data
# Pivot the data for the chart
df_pivot = df_master.pivot_table(index='Stock', columns='m_period', values='dividend_total', aggfunc='sum').fillna(0)

# Sort the columns based on period for proper order in plotting
sorted_columns = sorted(df_pivot.columns, key=lambda x: int(x[:-1]))
df_pivot = df_pivot[sorted_columns]

# Calculate the difference from one period to the next, filling NA with the original values for the first period
df_pivot_diff = df_pivot.diff(axis=1).fillna(0)
df_pivot_diff[sorted_columns[0]] = df_pivot[sorted_columns[0]]

# Plotting
fig, ax = plt.subplots(figsize=(10, 8))
df_pivot_diff.plot(kind='bar', stacked=True, ax=ax, color=colors_list)

# Customizations
ax.set_title('Dividend Total by Stock and Period', fontsize=16)
ax.set_xlabel('Stock', fontsize=14)
ax.set_ylabel('Dividend Total', fontsize=14)
ax.legend(title='Months Period', fontsize=12, loc='upper right')
plt.xticks(rotation=45)  # Ensure labels are rotated for readability

# Explicitly setting the x-axis labels if needed
ax.set_xticklabels(df_pivot_diff.index, rotation=45)

plt.tight_layout()  # Adjust layout
plt.savefig(f'{out_direc}/_G3_dividend_growth.png', dpi=300)
plt.show()  # Display the plot





# import matplotlib.pyplot as plt
# import pandas as pd

# # Convert to DataFrame

# # Using the provided pivot_table method from the user to create the df_pivot DataFrame
# df_pivot = df_master.pivot_table(index='Stock', columns='m_period', values='dividend_total', aggfunc='sum').fillna(0)

# # Sorting the columns based on the period to ensure correct subtraction
# sorted_columns = sorted(df_pivot.columns, key=lambda x: int(x[:-1]))
# df_pivot = df_pivot[sorted_columns]

# # Calculate the difference in dividends from one period to the next
# df_pivot_diff = df_pivot.diff(axis=1).fillna(0)

# # Since the first period (0m) has no previous data to subtract from, the difference will be set as the original values
# df_pivot_diff[sorted_columns[0]] = df_pivot[sorted_columns[0]]

# # # ############################################################################# # ############################################################################
# # # ############################################################################
# import matplotlib.pyplot as plt
# import pandas as pd

# colors_list = ['#0a2144', '#3070b6', '#ecc046', '#e9993e', '#86cdf2', '#a8aaa5', 
#                '#4eabe9', '#707070', '#5c96c8', '#3372b6', '#306fb5']
#  #Pivot the data for stacked bar chart

# # Plotting
# fig, ax = plt.subplots(figsize=(10, 8))
# df_pivot.plot(kind='bar', stacked=True, ax=ax)

# # Customization for clarity and professionalism
# ax.set_title('Dividend Total by Stock and Period', fontsize=16)
# ax.set_xlabel('Stock', fontsize=14)
# ax.set_ylabel('Dividend Total', fontsize=14)

# # Adjusting the legend position so it does not overlap with the chart
# ax.legend(title='Months Period', fontsize=12, loc='upper right')

# # Set the x-axis labels to rotate for better readability
# plt.xticks(rotation=45)

# # Apply a tight layout to adjust spacing
# plt.tight_layout()

# plt.savefig(f'{out_direc}/_G3_dividend_growth.png', dpi=300)




# # ############################################################################# # ############################################################################
# # ############################################################################# # ############################################################################# # ############################################################################
# # ############################################################################# # ############################################################################# # ############################################################################
# # ############################################################################


