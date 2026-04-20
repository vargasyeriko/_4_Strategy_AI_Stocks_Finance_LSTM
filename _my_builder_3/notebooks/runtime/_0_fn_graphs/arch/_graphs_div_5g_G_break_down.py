
import matplotlib.pyplot as plt
import pandas as pd

df_0 = _df_0m
# # ############################################################################# # ############################################################################
# # ############################################################################
# Portfolio labels to filter from df_0
    
portfolio_labels_g = ['AMC.AX', 'ALD.AX', 'ANZ.AX', 'APA.AX', 'BHP.AX','SQ2.AX', 
                    'BXB.AX', 'CHC.AX', 'COL.AX', 'CBA.AX', 
                    'CSL.AX', 'CSR.AX', 'IAG.AX', 'JLG.AX', '360.AX',
                    'PXA.AX', 'RHC.AX', 'RMD.AX', 'SHL.AX', 'TLS.AX', 
                    'TCL.AX', 'EX20.AX', 'WES.AX', 'VCX.AX', 'XRO.AX',
                    'QUAL.AX', 'ANN.AX', 'GLOB.AX', 'FEMX.AX', 'MCSI.XA',
                    'CLDD.AX','DJRE.AX', 'ACDC.AX',
                     'SEMI.AX','MIN.AX' ,'MQG.AX','TSLA','VHY.AX']

# # Filtering the DataFrame
portfolio_df_g = df_0[df_0['Stock'].isin(portfolio_labels_g)].copy()

# # GET PERCENTAGES
portfolio_df_g['Percentage'] = ((portfolio_df_g['units_hold'] / portfolio_df_g['units_hold'].sum()) * 100)

# # GRAPH
import matplotlib.pyplot as plt
import pandas as pd


# Colors provided by the user with the last two colors changed to green and red
colors =  [
    '#a11d1d', '#d36452', '#983912', '#d8935f', '#e9993e',
    '#cd9a56', '#ecc046', '#83793c', '#9d9d4f', '#84932a',
    '#a0c939', '#a8aaa5', '#5c8f19', '#32d8a9', '#259f8e',
    '#1bd1d1', '#278fa0', '#86cdf2', '#4a9ad6', '#3070b6',
    '#0a2144', '#1f3d88', '#5858d8', '#3f3096', '#5231a5',
    '#571688', '#7d4395', '#a04e94', '#b94d9a', '#b57da1',
    '#c3448c', 'pink', 'red']#, '#829231', '#34a477'


# Set the font to Arial for a more professional look
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 18  # Smaller font size for more stocks

# Create a pie chart with the adjusted font and styling, and larger figure size
fig, ax = plt.subplots(figsize=(25, 16))  # Larger figure size for readability
wedges, texts, autotexts = ax.pie(
    portfolio_df_g['units_hold'], labels=portfolio_df_g['Stock'], autopct='%1.1f%%',
    startangle=120, colors=colors, textprops={'fontsize': 12},  # Smaller font size for the labels
    wedgeprops={"edgecolor": "black", 'linewidth': 1}  # Optional: white line for separation between slices
)

# Improve legibility by setting the percentage color to white
for autotext in autotexts:
    autotext.set_color('white')

# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')

# Adjust the layout to make room for the legend
plt.tight_layout()

# Update legend labels to include the calculated percentages
legend_labels = [f'{row.Stock}:  ${row["units_hold"]:.1f} ({row["Percentage"]:.1f}%)' for index, row in portfolio_df_g.iterrows()]
ax.legend(legend_labels, title="Investment Amounts and Percentages", loc='center left', bbox_to_anchor=(.84, .57))

# Display the title
plt.title('Growht Portfolio Breakdown by Holding Value Percentages', fontsize=33, fontweight='bold', pad=37)

# Show the pie chart
#plt.show()


plt.savefig(f'{out_direc}/_G5g_Growht_breakdown_.png', dpi=300)




# # ############################################################################# # ############################################################################
# # ############################################################################# # ############################################################################# # ############################################################################
# # ############################################################################# # ############################################################################# # ############################################################################
# # ############################################################################


