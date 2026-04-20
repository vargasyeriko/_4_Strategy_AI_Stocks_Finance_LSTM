
import matplotlib.pyplot as plt
import pandas as pd

# Custom settings
font_size = 11
title_font_size = 33
title_font_weight = 'bold'
title_pad = 66
legend_location = 'center left'
bbox_to_anchor_custom = (0.84, 0.57)
figsize_custom = (25, 16)
start_angle = 120
edge_color = 'black'
line_width = .1
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
    '#c3448c', 'pink', 'red']

# List of stock codes
stocks = [
    '360.AX', 'ACDC.AX', 'ALD.AX', 'AMC.AX', 'ANN.AX', 'ANZ.AX', 'APA.AX', 'BHP.AX', 'BUGG.AX', 'BXB.AX',
    'CBA.AX', 'CHC.AX', 'CLDD.AX', 'COL.AX', 'CSL.AX', 'CSR.AX', 'DHOF.AX', 'DJRE.AX', 'EX20.AX', 'FEMX.AX',
    'GLOB.AX', 'GOLD.AX', 'GROW.AX', 'HCRD.AX', 'IAG.AX', 'IJH.AX', 'ILB.AX', 'JLG.AX', 'MCSI.XA', 'MIN.AX',
    'MQG.AX', 'MVA.AX', 'PXA.AX', 'QPON.AX', 'QUAL.AX', 'RHC.AX', 'RMD.AX', 'SEMI.AX', 'SHL.AX', 'SQ2.AX',
    'TACT.XA', 'TCL.AX', 'TLS.AX', 'TSLA', 'USIG.AX', 'VCX.AX', 'VHY.AX', 'WES.AX', 'XRO.AX'
]

def _g1_perc_pie_both(df_final):
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
        # Assuming df_group and other variables are already defined and you are within a plotting context
        total_hold = df_group['stock_value_hold'].sum()
        trans_cost = df_group['trans_fee'].iloc[0]  # Assuming 'trans_fee' is a column in df_group
    
        final_cash = df_group['period_cash'].iloc[0]
        final_dividends = df_group['period_divs'].iloc[0]
        
        # Creating the table at the bottom of the plot
        cell_text = [[f"${total_hold:.2f}", f"${trans_cost:.2f}"]]
        col_labels = ["Total Holds", "Brockage Costs"]
        col_widths = [0.2, 0.18]  # Adjust column widths to fit your data
        row_heights = 0.05  # Adjust row heights
    
    
        # FONT FOR BOTH 
        table = plt.table(cellText=cell_text, colLabels=col_labels, colWidths=col_widths,
                          loc='bottom', cellLoc='center', rowLoc='center',
                          bbox=[0.845, -.098, .172, 0.078])  # Bbox[x0, y0, width, height] to control the position and size
        
    
        plt.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.9)
        #
        #
        
        table = plt.table(cellText=[[f"${final_dividends:.2f}", f"${final_cash:.2f}"]], 
                          colLabels=["Dividends", "Cash"], colWidths=col_widths,
                          loc='bottom', cellLoc='center', rowLoc='center',
                          bbox=[0.645, -.098, .172, 0.078])  # Bbox[x0, y0, width, height] to control the position and size
        
    
        plt.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.9)
    
        #
        #
        #
        plt.title(f'Portfolio Breakdown for Period end Month ({analysis_end_date})', fontsize=title_font_size, fontweight=title_font_weight, pad=title_pad)
        file_path = f"_0_out/_0_pie_charts/_pie_{period}_{analysis_end_date.replace('/', '_')}.png"
        plt.savefig(file_path)
        #plt.show()

    
        
    
    















#########################
    
    # # Variables for the pie chart
    # final_cash = 34
    # final_dividends = 50
    
    # # Data to plot
    # labels_financial = ['Cash', 'Dividends']
    # sizes_financial = [final_cash, final_dividends]
    # colors_financial = ['limegreen', 'peachpuff']  # Custom colors
    # explode_financial = (0.1, 0)  # Explode the 1st slice (Cash)
    # # Modify autopct to display dollar amount first followed by percentage
    # autopct_financial = lambda p: f'${int(p * sum(sizes_financial) / 100)}\n({p:.1f}%)'
    # shadow_financial = True
    # startangle_financial = 320
    # textprops_financial = {'fontsize': 8, 'fontfamily': 'Arial', 'fontweight': 'normal'}  # Font size, family, and weight
    
    # # Figure and axis dimensions
    # figsize_financial_x = 3
    # figsize_financial_y = 3
    # ax_financial = plt.axes([0.6, 0.05, 0.2, 0.2])  # Adjusted bbox for the new chart position
    
    # # Pie chart
    # wedges_financial, labels_financial, _ = ax_financial.pie(sizes_financial, explode=explode_financial, labels=labels_financial, colors=colors_financial, autopct=autopct_financial,
    #          shadow=shadow_financial, startangle=startangle_financial, textprops=textprops_financial)
    
    # # Adjust the position of the labels individually
    # labels_financial[0].set_position((0.7, 1.1))  # Adjust position of "Cash"
    # labels_financial[1].set_position((.01, -1.3))  # Adjust position of "Dividends"
    
    # # Aspect ratio
    # ax_financial.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # ###### From this point, add on a new pie chart or other elements as needed.
    # # Adjusting the layout to make room for the table and pie chart
    # plt.subplots_adjust(left=.58, bottom=0.2, right=.93, top=0.9)
    
    # # Display the plot
    # plt.show()
