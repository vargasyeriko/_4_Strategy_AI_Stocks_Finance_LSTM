import matplotlib.pyplot as plt
import pandas as pd

# Custom settings
font_size = 14
title_font_size = 33
title_font_weight = 'bold'
title_pad = 66
legend_location = 'center left'
bbox_to_anchor_custom = (0.84, 0.57)
figsize_custom = (25, 16)
start_angle = 120
edge_color = 'black'
line_width = 1
text_color = 'white'
pct_distance_custom = 0.95
default_color = '#999999'  # Grey color for any undefined stock

# Setting the matplotlib parameters
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = font_size

# List of colors
colors = [
    '#a11d1d', '#d36452', '#983912', '#d8935f', '#e9993e',
    '#cd9a56', '#ecc046', '#83793c', '#9d9d4f', '#84932a',
    '#a0c939', '#a8aaa5', '#5c8f19', '#32d8a9', '#259f8e',
    '#1bd1d1', '#278fa0', '#86cdf2', '#4a9ad6', '#3070b6',
    '#0a2144', '#1f3d88', '#5858d8', '#3f3096', '#5231a5',
    '#571688', '#7d4395', '#a04e94', '#b94d9a', '#b57da1',
    '#c3448c', 'pink', 'red'
]

# List of stock codes
stocks = [
    '360.AX', 'ACDC.AX', 'ALD.AX', 'AMC.AX', 'ANN.AX', 'ANZ.AX', 'APA.AX', 'BHP.AX', 'BUGG.AX', 'BXB.AX',
    'CBA.AX', 'CHC.AX', 'CLDD.AX', 'COL.AX', 'CSL.AX', 'CSR.AX', 'DHOF.AX', 'DJRE.AX', 'EX20.AX', 'FEMX.AX',
    'GLOB.AX', 'GOLD.AX', 'GROW.AX', 'HCRD.AX', 'IAG.AX', 'IJH.AX', 'ILB.AX', 'JLG.AX', 'MCSI.XA', 'MIN.AX',
    'MQG.AX', 'MVA.AX', 'PXA.AX', 'QPON.AX', 'QUAL.AX', 'RHC.AX', 'RMD.AX', 'SEMI.AX', 'SHL.AX', 'SQ2.AX',
    'TACT.XA', 'TCL.AX', 'TLS.AX', 'TSLA', 'USIG.AX', 'VCX.AX', 'VHY.AX', 'WES.AX', 'XRO.AX'
]

# Create a dictionary mapping stocks to colors
color_mapping = {stock: colors[i % len(colors)] for i, stock in enumerate(stocks)}
color_mapping['CASH'] = '#00ff00'  # Bright green for 'CASH'

# Iterate over each period in df_final
for period, df_group in df_final.groupby('period'):
    # Exclude stocks with 0.000% percentage
    df_group = df_group[df_group['stock_value_hold_pct'] > 0.000]

    if df_group.empty:
        continue

    fig, ax = plt.subplots(figsize=figsize_custom)
    # Assign colors to each stock based on the color mapping
    plot_colors = [color_mapping.get(stock, default_color) for stock in df_group['Stock']]

    wedges, texts, autotexts = ax.pie(
        df_group['stock_value_hold'], labels=df_group['Stock'], autopct='%1.1f%%',
        startangle=start_angle, colors=plot_colors, textprops={'fontsize': font_size},
        wedgeprops={"edgecolor": edge_color, 'linewidth': line_width}, pctdistance=pct_distance_custom
    )

    for autotext in autotexts:
        autotext.set_color(text_color)

    ax.axis('equal')
    plt.tight_layout()

    legend_labels = [f'{row.Stock}: ${row.stock_value_hold:.1f} ({row.stock_value_hold_pct:.1f}%)' for index, row in df_group.iterrows()]
    ax.legend(legend_labels, title="Investment Amounts and Percentages", loc=legend_location, bbox_to_anchor=bbox_to_anchor_custom)

    
    analysis_end_date = df_group['AnalysisEndDate'].iloc[0]
    total_hold = df_group['stock_value_hold'].sum()
    trans_cost = df_group['trans_fee'].iloc[0]

    # Creating the table at the bottom of the plot
    cell_text = [[f"${total_hold:.2f}", f"${trans_cost:.2f}"]]
    col_labels = ["Total Holds", "Blockage Costs"]
    col_widths = [0.2, 0.18]  # Adjust column widths to fit your data
    row_heights = 0.05  # Adjust row heights
    
    table = plt.table(cellText=cell_text, colLabels=col_labels, colWidths=col_widths,
                      loc='bottom', cellLoc='center', rowLoc='center',
                      bbox=[0.845, -.098, .172, 0.078])  # Bbox[x0, y0, width, height] to control the position and size
    

    plt.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.9)
    plt.title(f'Growth Portfolio Breakdown for Period {period} ({analysis_end_date})', fontsize=title_font_size, fontweight=title_font_weight, pad=title_pad)
    file_path = f"_0_fn_graphs/_pie_{period}_{analysis_end_date.replace('/', '_')}.png"
    plt.savefig(file_path)
    plt.show()
