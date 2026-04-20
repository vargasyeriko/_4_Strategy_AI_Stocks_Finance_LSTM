# # ############################################################################
# # ############################################################################# # ############################################################################
# # ############################################################################
# Recalculating differences with added precision and additional comparisons
diff_6_to_12 = round(div_total_6 - div_total_12, 2)
diff_3_to_6 = round(div_total_3 - div_total_6, 2)
diff_0_to_3 = round(div_total_0 - div_total_3, 2)


# Calculating percentages for the differences
percentage_diff_6_to_12 = (diff_6_to_12 / div_total_12) * 100 if div_total_12 != 0 else 0
percentage_diff_3_to_6 = (diff_3_to_6 / div_total_6) * 100 if div_total_6 != 0 else 0
percentage_diff_0_to_3 = (diff_0_to_3 / div_total_3) * 100 if div_total_3 != 0 else 0

# Adjusting the dividends dictionary with the precise wording including percentage changes
dividends_updated_with_percentage = {
    f'12 Months AGO\nTotal: {round(div_total_12, 2)}': div_total_12,
    f'6 Months AGO\nDiff: {diff_6_to_12} ({round(percentage_diff_6_to_12, 2)}%)\nfrom 12 Months': div_total_6,
    f'3 Months AGO\nDiff: {diff_3_to_6} ({round(percentage_diff_3_to_6, 2)}%)\nfrom 6 Months': div_total_3,
    f'Today\nDiff: {diff_0_to_3} ({round(percentage_diff_0_to_3, 2)}%)\nfrom 3 Months': div_total_0,
}

# Updating the data preparation based on the new dictionary
months_updated_with_percentage = list(dividends_updated_with_percentage.keys())
values_updated_with_percentage = list(dividends_updated_with_percentage.values())

# Creating the updated bar plot with new labels and precise differentials including percentages
plt.figure(figsize=(12, 9))
bars_updated_with_percentage = plt.bar(range(len(months_updated_with_percentage)), values_updated_with_percentage, color=['red', 'orange', 'green', 'blue'])

plt.xlabel('Period', fontsize=16)
plt.ylabel('Total Dividends', fontsize=16)
plt.title('Dividend Growth Over Time with Percent Changes', fontsize=18)
plt.xticks(range(len(months_updated_with_percentage)), months_updated_with_percentage, fontsize=14, rotation=45, ha="right")
plt.yticks(fontsize=14)
plt.grid(axis='y', linestyle='--')

# Annotating the total values on top of each bar
for bar, value in zip(bars_updated_with_percentage, values_updated_with_percentage):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{round(value, 2)}', ha='center', va='bottom', fontsize=12)

plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
#plt.show()

# Before the plt.show() line, add the plt.savefig() function
plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels

# Save the figure as a PNG file with desired DPI for higher resolution
plt.savefig('_0_out/_G1_dividend_growth.png', dpi=300)

#plt.show()  # Display the plot

# # ############################################################################
# # ############################################################################# # ############################################################################
# # ############################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps as mcm
import datetime



# Creating a pivot table for proper alignment of stocks across periods
pivot_df = df_master.pivot_table(values='dividend_total', index='Stock', columns='m_period', fill_value=0)

# Assigning colors to each stock for consistency across plots
unique_stocks = pivot_df.index.tolist()
color_map = mcm.get_cmap('tab20')
colors = {stock: color_map(i / len(unique_stocks)) for i, stock in enumerate(unique_stocks)}

# Function to adjust color brightness
def adjust_color_brightness(color, brightness_factor):
    """Adjust the color brightness."""
    import colorsys
    try:
        c = np.array(colorsys.rgb_to_hls(*color[:3]))
        c[1] = max(0, min(1, c[1] * brightness_factor))
        return colorsys.hls_to_rgb(*c)
    except Exception:
        return color

# Plotting with color fading
fig, ax = plt.subplots(figsize=(12, 8))
bar_width = 0.1
offset = np.arange(len(unique_stocks))

periods = ['12m', '6m', '3m', '0m']
brightness_factors = [.30, 0.48, .70, .99]  # Starting from 12m to 0m

for i, period in enumerate(periods):
    faded_colors = [adjust_color_brightness(colors[stock], brightness_factors[i]) for stock in unique_stocks]
    ax.bar(offset + i*bar_width, pivot_df[period], width=bar_width, color=faded_colors, label=period)

    

    
    
# Finalizing the plot
ax.set_xticks(offset + 1.5*bar_width)
ax.set_xticklabels(unique_stocks, rotation=45, ha="right")
ax.set_xlabel('Stock')
ax.set_ylabel('Dividend Total')
ax.set_title('Dividend Totals by Stock and Period with Color Fading')
ax.legend(title='Period')


plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels
plt.show()
# Save the figure as a PNG file with desired DPI for higher resolution
plt.savefig('_0_out/_G2_dividend_growth.png', dpi=300)