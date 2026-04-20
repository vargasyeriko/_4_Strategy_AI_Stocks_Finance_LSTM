# # Example values
# end_period_value_april = 116047.03 # Assumed end of April period_stocks_value
# trans_fee_april = 0  # Assumed transaction fee for April
# diff_cash_montly_april = 238  # Assumed difference in cash for April

# start_period_value_march = 117948.11  # From your data
# net_cash_flow_april = diff_cash_montly_april - trans_fee_april

# # Monthly return calculation
# monthly_return_april = ((end_period_value_april - start_period_value_march - net_cash_flow_april) / start_period_value_march) * 100
# monthly_return_april





#### ############################################## CHECK after fetching prices 
# def check_nan_all():
#     ######################################## check days of the week missing data 
#     import pandas as pd
    
#     def check_nan_frequency(file_path):
#         # Load the DataFrame from a pickle file
#         df = pd.read_pickle(file_path)
        
#         # Prepare a dictionary to store the results
#         nan_frequency = {}
        
#         # Iterate over each column in the DataFrame
#         for column in df.columns:
#             # Drop non-NaN values and extract the weekday of NaN dates
#             nan_days = df[column][df[column].isna()].index.weekday
            
#             # Count the occurrences of each weekday
#             counts = nan_days.value_counts().sort_index()
            
#             # Map the weekday numbers to weekday names
#             weekday_names = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
#             counts.index = counts.index.map(weekday_names)
            
#             # Store the result in the dictionary
#             nan_frequency[column] = counts
        
#         return nan_frequency
    
#     # Example of how to use the function
#     file_path = "_1_fetch/_0_fetched_stock_data_prices.pkl"
#     nan_frequency = check_nan_frequency(file_path)
#     for stock, freq in nan_frequency.items():
#         print(f"NaN frequency for {stock}:\n{freq}\n")
    
    
#     ######################################## check Max consecutive days missing 
#     #
    
    
    
#     import pandas as pd
    
#     def max_consecutive_nans(file_path):
#         # Load the DataFrame from a pickle file
#         df = pd.read_pickle(file_path)
        
#         # Prepare a dictionary to store the results
#         max_nans = {}
        
#         # Iterate over each column in the DataFrame
#         for column in df.columns:
#             # Convert the column to boolean where True indicates NaN
#             is_nan = df[column].isna()
            
#             # Calculate consecutive NaNs using a custom method
#             # Using a cumulative sum of non-NaNs to define groups of consecutive NaNs
#             if is_nan.any():  # Only process if there are any NaNs at all
#                 max_nans[column] = (is_nan.groupby((is_nan != is_nan.shift()).cumsum()).cumsum()).max()
#             else:
#                 max_nans[column] = 0
        
#         return max_nans
    
#     # Mother function to orchestrate the reading and processing
#     def analyze_stock_data(file_path):
#         # Get maximum consecutive NaNs
#         max_consecutive_nans_result = max_consecutive_nans(file_path)
        
#         return max_consecutive_nans_result
    
#     # Example of how to use the mother function
#     file_path = "_1_fetch/_0_fetched_stock_data_prices.pkl"
#     result = analyze_stock_data(file_path)
#     for stock, max_nan in result.items():
#         print(f"Maximum consecutive NaN days for {stock}: {max_nan}")

#


#
#
##############################################################################################
##############################################################################################
##############################################################################################
##############################################################################################
# _#_FN NAME ****** 9999 <<<      - sum units sold by stock -        >>> 9999 **********
############################ *********************************** #############################
######################################### - - - ##############################################
#
#
# import pandas as pd

# def calculate_and_add_dividends(df):
#     # Specify the path to your dividend data pickle file
#     file_path = '_1_fetch/_1_fetched_stock_dividend_percentages.pkl'
    
#     # Load the dividend data from the pickle file
#     dividend_data = pd.read_pickle(file_path)

#     def get_dividends(row):
#         # Filter the dividend data for the specified stock and within the date range
#         applicable_dividends = dividend_data[
#             (dividend_data.index >= row['StartDate']) & 
#             (dividend_data.index <= row['AnalysisEndDate'])
#         ].get(row['Stock'], pd.Series(dtype='float64')).sum()
#         return applicable_dividends

#     # Check if 'units_hold' column exists, if not add it and set to 1
#     if 'units_hold' not in df.columns:
#         df['units_hold'] = 1  # Default to 1 if not present
#         print("\n*ATTN*\n**\n* No 'units_hold' column found, setting all units to 1.")

#     # Calculate dividends for each row and apply units_hold factor
#     df['Dividends'] = df.apply(get_dividends, axis=1) * df['units_hold']

#     return df


########### check divs
# import yfinance as yf

# def fetch_total_dividends(stock_ticker, start_date, end_date):

#     # Load the stock data
#     stock = yf.Ticker(stock_ticker)
    
#     # Fetch the dividends data
#     dividends = stock.dividends[start_date:end_date]
    
#     # Calculate the total dividends paid
#     total_dividends = dividends.sum()
    
#     return total_dividends

# fetch_total_dividends('ACDC.AX', '2024-04-01',  '2024-05-02')#*235.817818
# fetch_total_dividends('QPON.AX', '2022-07-01',  '2022-07-02')*219.184632
# fetch_total_dividends('MVA.AX', '2022-07-01',  '2022-07-02')*148.334983

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


# Create a dictionary mapping stocks to colors
color_mapping = {stock: colors[i % len(colors)] for i, stock in enumerate(stocks)}
color_mapping['CASH'] = '#00ff00'  # Bright green for 'CASH'



# Setting the matplotlib parameters
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = font_size

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

#

# CASH AND DIVS
# Data to plot 
labels_cd = ['Cash', 'Dividends']
colors_cd = ['limegreen', 'peachpuff']  # Custom colors
explode_cd = (0.3, 0)  # Explode the 1st slice (Cash)
# Modify autopct to display dollar amount first followed by percentage
autopct_cd = lambda p: f'${int(p * sum(sizes_cd) / 100)}\n({p:.1f}%)'
shadow_cd = True
startangle_cd = 320
textprops_cd = {'fontsize': 8, 'fontfamily': 'Arial', 'fontweight': 'normal'}  # Font size, family, and weight



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

    ending_cash = df_group['period_cash'].iloc[0]
    ending_dividends = df_group['period_divs'].iloc[0]
    sizes_cd = [ending_cash, ending_dividends]
    ########################################### DIV / CASH
    # Figure and axis dimensions
    figsize_x = 3
    figsize_y = 3
    #
    ax2 = plt.axes([0.6, 0.05, 0.2, 0.2])  # Adjusted bbox for the new chart position
    
    # Pie chart
    wedges, labels, autopct_labels = ax2.pie(sizes_cd, explode=explode_cd, labels=labels_cd, 
                                             colors=colors_cd, autopct=autopct_cd,
                                             shadow=shadow_cd, startangle=startangle_cd,textprops=textprops_cd)
    
    # Adjust the position of the labels individually
    labels[0].set_position((0.7, 1.1))  # Adjust position of "Cash"
    labels[1].set_position((.01, -1.3))  # Adjust position of "Dividends"
    
    #autopct[0].set_position((0.7, 1.1))
    # # Adjust the position of the autopct labels individually
    # for i, autopct in enumerate(autopct_labels):
    #     if i == 0:
    #         autopct.set_position((0.1, 0.1))  # Adjust the position of the first autopct label
    #     elif i == 1:
    #         autopct.set_position((-0.1, -0.1))  # Adjust the position of the second autopct label
    
    # Aspect ratio
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    # Adjusting the layout to make room for the table and pie chart
    plt.subplots_adjust(left=0.1, bottom=0.2, right=.9, top=0.9)
    
    # Display the plot
    #plt.show()

    ##########################
    ###########################
    
    # Creating the table at the bottom of the plot
    cell_text = [[f"${total_hold:.2f}", f"${trans_cost:.2f}"]]
    col_labels = ["Total Holds", "Blockage Costs"]
    col_widths = [0.2, 0.18]  # Adjust column widths to fit your data
    row_heights = 0.05  # Adjust row heights
    
    table = plt.table(cellText=cell_text, colLabels=col_labels, colWidths=col_widths,
                      loc='bottom', cellLoc='center', rowLoc='center',
                      bbox=[0.845, -.098, .172, 0.078])  # Bbox[x0, y0, width, height] to control the position and size
    
    # # Creating the second table
    # cell_text2 = [[f"${ending_cash:.2f}", f"${ending_dividends:.2f}"]]
    # col_labels2 = ["Cash Amount", "Dividends"]
    # col_widths2 = [0.2, 0.18]
    # table2 = plt.table(cellText=cell_text2, colLabels=col_labels2, colWidths=col_widths2,
    #                    loc='bottom', cellLoc='center', rowLoc='center',
    #                    bbox=[0.6, -0.098, 0.172, 0.078])  
    
    # # Adjusting the layout to make room for the table
    # plt.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.9)
    #
    #
    plt.title(f'Growth Portfolio Breakdown for Period {period} ({analysis_end_date})', fontsize=title_font_size, fontweight=title_font_weight, pad=title_pad)
    file_path = f"_0_fn_graphs/_pie_{period}_{analysis_end_date.replace('/', '_')}.png"
    plt.savefig(file_path)
    plt.show()

#input("Press Enter to continue to the next chart...")


# import matplotlib.pyplot as plt
# import pandas as pd

# # Custom settings
# font_size = 14
# title_font_size = 33
# title_font_weight = 'bold'
# title_pad = 66
# legend_location = 'center left'
# bbox_to_anchor_custom = (0.84, 0.57)
# figsize_custom = (25, 16)
# start_angle = 120
# edge_color = 'black'
# line_width = 1
# text_color = 'white'
# pct_distance_custom = 0.95
# default_color = '#999999'  # Grey color for any undefined stock

# # Setting the matplotlib parameters
# plt.rcParams['font.family'] = 'Arial'
# plt.rcParams['font.size'] = font_size

# # List of colors
# colors = [
#     '#a11d1d', '#d36452', '#983912', '#d8935f', '#e9993e',
#     '#cd9a56', '#ecc046', '#83793c', '#9d9d4f', '#84932a',
#     '#a0c939', '#a8aaa5', '#5c8f19', '#32d8a9', '#259f8e',
#     '#1bd1d1', '#278fa0', '#86cdf2', '#4a9ad6', '#3070b6',
#     '#0a2144', '#1f3d88', '#5858d8', '#3f3096', '#5231a5',
#     '#571688', '#7d4395', '#a04e94', '#b94d9a', '#b57da1',
#     '#c3448c', 'pink', 'red']

# # List of stock codes
# stocks = [
#     '360.AX', 'ACDC.AX', 'ALD.AX', 'AMC.AX', 'ANN.AX', 'ANZ.AX', 'APA.AX', 'BHP.AX', 'BUGG.AX', 'BXB.AX',
#     'CBA.AX', 'CHC.AX', 'CLDD.AX', 'COL.AX', 'CSL.AX', 'CSR.AX', 'DHOF.AX', 'DJRE.AX', 'EX20.AX', 'FEMX.AX',
#     'GLOB.AX', 'GOLD.AX', 'GROW.AX', 'HCRD.AX', 'IAG.AX', 'IJH.AX', 'ILB.AX', 'JLG.AX', 'MCSI.XA', 'MIN.AX',
#     'MQG.AX', 'MVA.AX', 'PXA.AX', 'QPON.AX', 'QUAL.AX', 'RHC.AX', 'RMD.AX', 'SEMI.AX', 'SHL.AX', 'SQ2.AX',
#     'TACT.XA', 'TCL.AX', 'TLS.AX', 'TSLA', 'USIG.AX', 'VCX.AX', 'VHY.AX', 'WES.AX', 'XRO.AX'
# ]

# # Create a dictionary mapping stocks to colors
# color_mapping = {stock: colors[i % len(colors)] for i, stock in enumerate(stocks)}
# color_mapping['CASH'] = '#00ff00'  # Bright green for 'CASH'

# # Iterate over each period in df_final
# for period, df_group in df_final.groupby('period'):
#     # Exclude stocks with 0.000% percentage
#     df_group = df_group[df_group['stock_value_hold_pct'] > 0.000]

#     if df_group.empty:
#         continue

#     fig, ax = plt.subplots(figsize=figsize_custom)
#     # Assign colors to each stock based on the color mapping
#     plot_colors = [color_mapping.get(stock, default_color) for stock in df_group['Stock']]

#     wedges, texts, autotexts = ax.pie(
#         df_group['stock_value_hold'], labels=df_group['Stock'], autopct='%1.1f%%',
#         startangle=start_angle, colors=plot_colors, textprops={'fontsize': font_size},
#         wedgeprops={"edgecolor": edge_color, 'linewidth': line_width}, pctdistance=pct_distance_custom
#     )

#     for autotext in autotexts:
#         autotext.set_color(text_color)

#     ax.axis('equal')
#     plt.tight_layout()

#     legend_labels = [f'{row.Stock}: ${row.stock_value_hold:.1f} ({row.stock_value_hold_pct:.1f}%)' for index, row in df_group.iterrows()]
#     ax.legend(legend_labels, title="Investment Amounts and Percentages", loc=legend_location, bbox_to_anchor=bbox_to_anchor_custom)

    
#     analysis_end_date = df_group['AnalysisEndDate'].iloc[0]
#     # Assuming df_group and other variables are already defined and you are within a plotting context
#     total_hold = df_group['stock_value_hold'].sum()
#     trans_cost = df_group['trans_fee'].iloc[0]  # Assuming 'trans_fee' is a column in df_group

#     ending_cash = df_group['period_cash'].iloc[0]
#     ending_dividends = df_group['period_divs'].iloc[0]
    
#     # Creating the table at the bottom of the plot
#     cell_text = [[f"${total_hold:.2f}", f"${trans_cost:.2f}"]]
#     col_labels = ["Total Holds", "Blockage Costs"]
#     col_widths = [0.2, 0.18]  # Adjust column widths to fit your data
#     row_heights = 0.05  # Adjust row heights
    
#     table = plt.table(cellText=cell_text, colLabels=col_labels, colWidths=col_widths,
#                       loc='bottom', cellLoc='center', rowLoc='center',
#                       bbox=[0.845, -.098, .172, 0.078])  # Bbox[x0, y0, width, height] to control the position and size
    
#     # Creating the second table
#     cell_text2 = [[f"${cash_amount:.2f}", f"${cdiv_amount:.2f}"]]
#     col_labels2 = ["Cash Amount", "Dividends"]
#     col_widths2 = [0.2, 0.18]
#     table2 = plt.table(cellText=cell_text2, colLabels=col_labels2, colWidths=col_widths2,
#                        loc='bottom', cellLoc='center', rowLoc='center',
#                        bbox=[0.6, -0.098, 0.172, 0.078])  
    
#     # Adjusting the layout to make room for the table
#     plt.subplots_adjust(left=0.1, bottom=0.2, right=0.9, top=0.9)
#     #
#     #
#     plt.title(f'Growth Portfolio Breakdown for Period {period} ({analysis_end_date})', fontsize=title_font_size, fontweight=title_font_weight, pad=title_pad)
#     file_path = f"_0_fn_graphs/_pie_{period}_{analysis_end_date.replace('/', '_')}.png"
#     plt.savefig(file_path)
#     plt.show()

#     #input("Press Enter to continue to the next chart...")




import matplotlib.pyplot as plt

# Variables
cash = 34
div = 50

# Data to plot
labels = 'Cash', 'Dividends'
sizes = [cash, div]
colors = ['limegreen', 'peachpuff']  # Updated colors
explode = (0.1, 0)  # explode the 1st slice (Cash)

# Plot
plt.figure(figsize=(2, 2))  # specifying a smaller figure size
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)

plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()

import pandas as pd
import matplotlib.pyplot as plt

# Sample DataFrame
data = {
    'Stock': ['360.AX', 'ACDC.AX', 'ALD.AX', 'AMC.AX', 'ANN.AX', 'ANZ.AX']*4,  # Repeating for different periods
    'AnalysisEndDate': ['2024-05-09']*24,
    'period': [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 6, 6, 6, 6, 6, 6, 12, 12, 12, 12, 12, 12],
    'stock_value_hold': [100, 200, 300, 400, 500, 600]*4,
    'period_cash': [10, 20, 30, 40, 50, 60]*4,
    'period_divs': [1, 2, 3, 4, 5, 6, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 1.2, 2.3, 3.4, 4.5, 5.6, 6.7, 1.3, 2.4, 3.5, 4.6, 5.7, 6.8],
    'stock_value_hold_pct': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]*4,
    'trans_fee': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]*4
}
df_final = pd.DataFrame(data)

# Pivot the data to get sums of dividends for each stock and selected periods
df_pivot = df_final.pivot_table(values='period_divs', index='Stock', columns='period', aggfunc='sum')

# Filter only required periods
df_pivot = df_pivot[[0, 3, 6, 12]]

# Color mapping (one color per stock, needs to align with the number of stocks)
colors = [
    '#a11d1d', '#d36452', '#983912', '#d8935f', '#e9993e',
    '#cd9a56', '#ecc046', '#83793c', '#9d9d4f', '#84932a',
    '#a0c939', '#a8aaa5', '#5c8f19', '#32d8a9', '#259f8e',
    '#1bd1d1', '#278fa0', '#86cdf2', '#4a9ad6', '#3070b6',
    '#0a2144', '#1f3d88', '#5858d8', '#3f3096', '#5231a5',
    '#571688', '#7d4395', '#a04e94', '#b94d9a', '#b57da1',
    '#c3448c', 'pink', 'red'
]

# Plotting
fig, ax = plt.subplots(figsize=(10, 8))
df_pivot.plot(kind='bar', stacked=True, ax=ax, color=colors[:len(df_pivot.index)])

# Customizations
ax.set_title('Dividend Total by Stock and Period', fontsize=16)
ax.set_xlabel('Stock', fontsize=14)
ax.set_ylabel('Dividend Total', fontsize=14)
ax.legend(title='Months Period', fontsize=12, loc='upper right')
plt.xticks(rotation=45)  # Ensure labels are rotated for readability

plt.tight_layout()  # Adjust layout
plt.show()


########## calculate compund return 
import pandas as pd

def calculate_compound_return(df):
    # Ensure the DataFrame is sorted by date
    df = df.sort_values(by='AnalysisEndDate')
    
    # Ask the user for the start and end periods
    start_period = int(input("Enter the start period (number of months ago): "))
    end_period = int(input("Enter the end period (number of months ago): "))
    
    # Ensure start_period is earlier than end_period
    if start_period > end_period:
        start_period, end_period = end_period, start_period
    
    # Ensure the periods are within the DataFrame range
    if start_period < 0 or end_period < 0 or start_period >= len(df) or end_period >= len(df):
        raise ValueError("Periods are out of range.")
    
    # Filter the DataFrame to the specified periods
    df_filtered = df.iloc[-(end_period+1):-(start_period) if start_period != 0 else None].reset_index(drop=True)
    
    # Calculate the compound return using the specified formula
    compound_return = (df_filtered['return_percentage'] / 100 + 1).prod() - 1
    
    # Get the start and end dates from the filtered DataFrame
    start_date = df_filtered['AnalysisEndDate'].iloc[0]
    end_date = df_filtered['AnalysisEndDate'].iloc[-1]
    
    return f"The compound return from {start_date.date()} to {end_date.date()} is {compound_return * 100:.2f}%"



