

# # ############################################################################# # ############################################################################
# # ############################################################################
# Defining the colors list as provided
colors_list = ['#0a2144', '#3070b6', '#ecc046', '#e9993e', '#86cdf2', '#a8aaa5', 
               '#4eabe9', '#707070', '#5c96c8', '#3372b6', '#306fb5']

# Given DataFrame name is df_ret, re-using the previously defined DataFrame as df_ret for this example
df_ret['CashBucket'] = df_ret['TotalDiv']  +df_ret['cash'] 
df_ret['TotalPortfolioValue'] = df_ret['TotalHoldingValue'] + df_ret['CashBucket']

# Plotting with adjustments
plt.figure(figsize=(12, 8))

# Plotting TotalPortfolioValue with the updated approach
plt.plot(df_ret['AnalysisEndDate'], df_ret['TotalPortfolioValue'], label='Total Portfolio Value', 
         color=colors_list[1], marker='o')

# Setting custom ticks on the x-axis to show only the dates from df_ret
plt.xticks(df_ret['AnalysisEndDate'])

# Adding a grid for readability
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Dynamically adding legend entries for each point
for index, row in df_ret.iterrows():
    plt.text(row['AnalysisEndDate'], row['TotalPortfolioValue'], 
             f"{row['AnalysisEndDate'].strftime('%Y-%m-%d')}\nCash: {row['CashBucket']:.2f}\nRETURN: {row['TotalHoldingValue']:.2f}",
             color='green', fontsize=15, ha='left')

# Setting title and labels with specified colors
plt.title('Portfolio Total Value Over Time', fontsize=14, color=colors_list[0])
plt.xlabel('Date', fontsize=12, color=colors_list[0])
plt.ylabel('Total Portfolio Value', fontsize=12, color=colors_list[0])

plt.tight_layout()
#plt.show()


plt.savefig(f'{out_direc}/_G4_return_hist.png', dpi=300)




# # ############################################################################# # ############################################################################
# # ############################################################################# # ############################################################################# # ############################################################################
# # ############################################################################# # ############################################################################# # ############################################################################
# # ############################################################################


