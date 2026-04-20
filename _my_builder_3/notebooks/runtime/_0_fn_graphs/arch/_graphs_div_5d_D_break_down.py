
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches



# # ############################################################################# # ############################################################################
# # ############################################################################
df_0 = _df_0m
# Portfolio labels to filter from df_0
portfolio_labels_d = ['DHOF.AX', 'ILB.AX', 'QPON.AX', 'TACT.XA', 
                      'GROW.AX', 'MVA.AX', 'GOLD.AX','HCRD.AX','USIG.AX']

# Filtering the DataFrame
portfolio_df_d = df_0[df_0['Stock'].isin(portfolio_labels_d)].copy()
# # GET PERCENTAGES
portfolio_df_d['Percentage'] = ((portfolio_df_d['units_hold'] / portfolio_df_d['units_hold'].sum()) * 100)

# GRAPH
colors = ['#0a2144', '#3070b6', '#ecc046', '#e9993e', '#86cdf2', '#a8aaa5', '#b57da1', 'pink', 'red']

# Set the font to Arial for a more professional look
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 18  # Adjusted font size for more stocks

# Create a pie chart with a larger figure size for readability
fig, ax = plt.subplots(figsize=(25, 16))
wedges, texts, autotexts = ax.pie(
    portfolio_df_d['units_hold'], 
    labels=portfolio_df_d['Stock'], 
    autopct='%1.1f%%',
    startangle=35, 
    colors=colors,
    textprops={'fontsize': 16},  # Smaller font size for the labels
    wedgeprops={"edgecolor": "black", 'linewidth': 1}  # Black line for separation between slices
)

# Set the percentage color to white for legibility
for autotext in autotexts:
    autotext.set_color('white')

# Ensure the pie chart is drawn as a circle
ax.axis('equal')

# Adjust the layout to make room for the legend outside the pie chart
plt.tight_layout()

# Create a legend with the actual amounts and percentages
legend_labels = [f'{row.Stock}: ${row["units_hold"]:.1f} ({row["Percentage"]:.1f}%)' 
                 for index, row in portfolio_df_d.iterrows()]

# Create custom handles for the legend to get a table-like look
handles = [mpatches.Patch(color=colors[i], label=legend_labels[i]) for i in range(len(legend_labels))]

# Display the legend with a frame and custom settings for a table-like appearance
leg = ax.legend(handles=handles, title="Investment Amounts", loc='center left', bbox_to_anchor=(.000012,.84),
                borderaxespad=0.2, handletextpad=5, labelspacing=1.1)
leg.get_frame().set_linewidth(1)  # Set a border for the legend

# Display the title with adjusted font size and weight
plt.title('Portfolio Breakdown by Net Cash Value', fontsize=33, fontweight='bold', pad=46)

# Show the pie chart
#plt.show()

# CASH in HERE !!! 

plt.savefig(f'{out_direc}/_G5d_Defensive_breakdown_.png', dpi=300)




# # ############################################################################# # ############################################################################
# # ############################################################################# # ############################################################################# # ############################################################################
# # ############################################################################# # ############################################################################# # ############################################################################
# # ############################################################################


