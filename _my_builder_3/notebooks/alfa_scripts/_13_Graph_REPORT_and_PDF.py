
# import matplotlib.pyplot as plt
# import pandas as pd 
# df = pd.read_pickle(f'_1_tables/_df_report_3_ret_div_cash_.pkl')

# # exec(open(f"_0_fn_graphs/_graphs_div_1_2.py",encoding="utf-8").read())

# # exec(open(f"_0_fn_graphs/_graphs_div_31_added.py",encoding="utf-8").read())

# # exec(open(f"_0_fn_graphs/_graphs_div_4_return_hist_.py",encoding="utf-8").read())

# # exec(open(f"_0_fn_graphs/_graphs_div_5d_D_break_down.py",encoding="utf-8").read())

# # exec(open(f"_0_fn_graphs/_graphs_div_5g_G_break_down.py",encoding="utf-8").read())


# # PDF

# #exec(open(f"_14_Graphs_and_PDF.py",encoding="utf-8").read())
# df_all =df.copy()

# df_all.head()
# brokerage_paid = 700 #do function 
# initial_investment= 100000 - brokerage_paid
# d_start_date= '2022-07-01'

# # Monthly returns table 
# df = df.drop_duplicates(subset=['period'], keep='first')
# df = df[['AnalysisEndDate','period', 'period_cash' ,
#        'period_divs','period_total_cash',
#        'period_stocks_value','period_total_holds'
#       ]]
# ######################################################
# ###############################################################

# per_inv = len(df)
# new_row = {
#     "AnalysisEndDate": d_start_date,
#     "period": per_inv,  # Assigning -1 to denote initial state before period 0
#     "period_cash": 0,
#     "period_divs": 0,
#     "period_total_cash": 0,
#     "period_stocks_value": 0,
#     "period_total_holds": initial_investment
# }

# # Appending the new row
# df = df.append(new_row, ignore_index=True)
# df.sort_values(by='period', ascending=True, inplace=True)
# # Calculate monthly returns
# df['previous_total_holds'] = df['period_total_holds'].shift(-1)
# # 

# # MONTHLY RETURNS full AMOUNT
# df['monthly_return'] = ((df['period_total_holds'] - df['previous_total_holds']) / df['previous_total_holds']) * 100
# df['total_return'] = ((df['period_total_holds']/initial_investment)-1)*100

# ######################################################
# ###############################################################
# import pandas as pd

# # Assuming 'df' is your DataFrame and 'AnalysisEndDate' contains date as string
# # Convert 'AnalysisEndDate' to datetime just once for the whole DataFrame
# df['AnalysisEndDate'] = pd.to_datetime(df['AnalysisEndDate'])

# # Get the first and last date from the DataFrame
# start_date = df.iloc[1]['AnalysisEndDate']
# end_date = df.iloc[0]['AnalysisEndDate']

# # Since start_date and end_date are already datetime objects, you can directly use them
# # Extract the day of the month for both start and end dates
# start_day = start_date.day
# end_day = end_date.day

# # Format these dates to extract month and year
# start_month = start_date.strftime('%B %Y')
# end_month = end_date.strftime('%B %Y')

# # Get the return percentage from the first recordable calculation
# total_return = df.iloc[0]['monthly_return']  # This picks the latest month's return

# # Create the message
# message_mr = f"""The total return of the fund including dividends and,
# cash flow from {start_date.strftime('%d %B %Y')} to {end_date.strftime('%d %B %Y')}, was: {total_return:.2f}%
# """
# #print(message_mr)


######################################################
# ###############################################################
# import pandas as pd

# # Assuming 'df' is your DataFrame and 'AnalysisEndDate' contains date as string
# # Convert 'AnalysisEndDate' to datetime just once for the whole DataFrame
# df['AnalysisEndDate'] = pd.to_datetime(df['AnalysisEndDate'])

# # Get the first and last date from the DataFrame
# start_date = df.iloc[-1]['AnalysisEndDate']
# end_date = df.iloc[0]['AnalysisEndDate']

# # Since start_date and end_date are already datetime objects, you can directly use them
# # Extract the day of the month for both start and end dates
# start_day = start_date.day
# end_day = end_date.day

# # Format these dates to extract month and year
# start_month = start_date.strftime('%B %Y')
# end_month = end_date.strftime('%B %Y')

# # # Get the return percentage from the first recordable calculation
# # total_return = df.iloc[0]['total_return']  # This picks the latest month's return

# # # Create the message
# # message_tr = f"""The total return of the fund including dividends and,
# # cash flow from {start_date.strftime('%d %B %Y')} to {end_date.strftime('%d %B %Y')}, was: {total_return:.2f}%
# # """
# # #print(message_tr)


# ######################################################
# ###############################################################

# # import pandas as pd

# # # Assuming 'df' is your DataFrame and 'AnalysisEndDate' contains date as string
# # # Convert 'AnalysisEndDate' to datetime just once for the whole DataFrame
# # df['AnalysisEndDate'] = pd.to_datetime(df['AnalysisEndDate'])

# # # Get the first and last date from the DataFrame
# # start_date = df.iloc[-1]['AnalysisEndDate']
# # end_date = df.iloc[0]['AnalysisEndDate']

# # # Since start_date and end_date are already datetime objects, you can directly use them
# # # Extract the day of the month for both start and end dates
# # start_day = start_date.day
# # end_day = end_date.day

# # # Format these dates to extract month and year
# # start_month = start_date.strftime('%B %Y')
# # end_month = end_date.strftime('%B %Y')

# # # Get the return percentage from the first recordable calculation
# # total_return_stocks = df.iloc[0]['period_stocks_value']  # This picks the latest month's return

# # # Create the message
# # message_psr = f"""The total Stock Holding Value from {start_date.strftime('%d %B %Y')} to {end_date.strftime('%d %B %Y')}, was: {total_return_stocks:.2f} $
# # """
# #print(message)

# ######################################################
# ###############################################################

# import pandas as pd

# # Assuming 'df' is your DataFrame and 'AnalysisEndDate' contains date as string
# # Convert 'AnalysisEndDate' to datetime just once for the whole DataFrame
# df['AnalysisEndDate'] = pd.to_datetime(df['AnalysisEndDate'])

# # Get the first and last date from the DataFrame
# start_date = df.iloc[-1]['AnalysisEndDate']
# end_date = df.iloc[0]['AnalysisEndDate']

# # Since start_date and end_date are already datetime objects, you can directly use them
# # Extract the day of the month for both start and end dates
# start_day = start_date.day
# end_day = end_date.day

# # Format these dates to extract month and year
# start_month = start_date.strftime('%B %Y')
# end_month = end_date.strftime('%B %Y')

# # Get the return percentage from the first recordable calculation
# total_return_divs = df.iloc[0]['period_divs']  # This picks the latest month's return

# # Create the message
# message_psd = f"""The total Dividends from {start_date.strftime('%d %B %Y')} to {end_date.strftime('%d %B %Y')}, was: {total_return_divs:.2f} $
# """
# #print(message)
# ######################################################
# ###############################################################

import pandas as pd

# Assuming 'df' is your DataFrame and 'AnalysisEndDate' contains date as string
# Convert 'AnalysisEndDate' to datetime just once for the whole DataFrame
df['AnalysisEndDate'] = pd.to_datetime(df['AnalysisEndDate'])

# Get the first and last date from the DataFrame
start_date = df.iloc[-1]['AnalysisEndDate']
end_date = df.iloc[0]['AnalysisEndDate']

# Since start_date and end_date are already datetime objects, you can directly use them
# Extract the day of the month for both start and end dates
start_day = start_date.day
end_day = end_date.day

# Format these dates to extract month and year
start_month = start_date.strftime('%B %Y')
end_month = end_date.strftime('%B %Y')

# Get the return percentage from the first recordable calculation
total_return = df.iloc[0]['period_cash']  # This picks the latest month's return

# Create the message
message_pcb = f"""The total Cash Balance from {start_date.strftime('%d %B %Y')} to {end_date.strftime('%d %B %Y')}, was: {total_return:.2f} $
"""
#print(message)
######################################################
###############################################################
# Assuming 'df' is your DataFrame and 'AnalysisEndDate' contains date as string
# Convert 'AnalysisEndDate' to datetime just once for the whole DataFrame
df['AnalysisEndDate'] = pd.to_datetime(df['AnalysisEndDate'])

# Get the first and last date from the DataFrame
start_date = df.iloc[-1]['AnalysisEndDate']
end_date = df.iloc[0]['AnalysisEndDate']

# Since start_date and end_date are already datetime objects, you can directly use them
# Extract the day of the month for both start and end dates
start_day = start_date.day
end_day = end_date.day

# Format these dates to extract month and year
start_month = start_date.strftime('%B %Y')
end_month = end_date.strftime('%B %Y')

# Get the return percentage from the first recordable calculation
total_return = df.iloc[0]['period_total_cash']  # This picks the latest month's return

# Create the message
message_pca = f"""The total Cash Amount accouting for Dividends and Cash Flow was: {total_return:.2f} $
"""
#print(message)


######################################################
###############################################################
# CAGR

# Get the first and last date from the DataFrame
start_date = df.iloc[-1]['AnalysisEndDate']
end_date = df.iloc[0]['AnalysisEndDate']

final_value = total_return_stocks
dividends_received = total_return_divs

total_adjusted_final = final_value - initial_investment + dividends_received - brokerage_paid
time_difference = (end_date - start_date).days / 365.25  # Use 365.25 to account for leap years

CAGR = ((final_value + dividends_received - brokerage_paid) / initial_investment) ** (1 / time_difference) - 1
CAGR_percentage = CAGR * 100

message_cagr =f"""
The Compound Annual Growth Rate (CAGR) for the portfolio
from {start_date.strftime('%d %B %Y')} to {end_date.strftime('%d %B %Y')} is approximately {CAGR_percentage:.2f}% per annum
"""


######################################################
###############################################################
report_p1 = f"""
*********************************************************************

Assuming Balance Growth, we have the following:

Portfolio Initial investment is: ${initial_investment+brokerage_paid} 
Approximately, we have blockage costs of: ${brokerage_paid}

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


######################################################
############################################################### MAIN GRAPH 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import numpy as np

# Assume df is your existing DataFrame with the correct data
# df should have columns: 'AnalysisEndDate', 'total_return', 'Benchmark'

# Remove the last row from the DataFrame
#df = df.iloc[:-1]
# Assuming Benchmark is 95% of 'Growth 97 Model Portfolio'
df['Benchmark'] = df['total_return'] * 0.95
# Ensure 'AnalysisEndDate' is a datetime type for proper plotting
df['AnalysisEndDate'] = pd.to_datetime(df['AnalysisEndDate'])

# Plotting
plt.style.use('ggplot')
fig = plt.figure(tight_layout=True, figsize=(12, 8))
gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])

ax1 = fig.add_subplot(gs[0])
ax1.plot(df['AnalysisEndDate'], df['total_return'], label='Total Return', color='blue', marker='o', linewidth=0.8)
ax1.plot(df['AnalysisEndDate'], df['Benchmark'], label='Benchmark', color='orange', marker='o', linewidth=0.8)
ax1.set_title('Growth of Investment Over Time', fontsize=16)
ax1.set_xlabel('Date', fontsize=12)
ax1.set_ylabel('Dollar Value', fontsize=12)
ax1.legend()

# Adding monthly vertical lines
dates = df['AnalysisEndDate']
for date in dates:
    ax1.axvline(x=date, color='gray', linestyle='--', linewidth=0.5)

# Generating synthetic monthly performance data for demonstration (you can replace this with actual data)
monthly_performance = np.random.uniform(0.3, 1.5, len(dates)).round(2)
performance_data = {
    'Months': dates.dt.strftime('%Y-%m'),  # Corrected use of strftime
    'Performance': [f"{p}%" for p in monthly_performance]
}

performance_df = pd.DataFrame(performance_data)

ax2 = fig.add_subplot(gs[1])
ax2.axis('tight')
ax2.axis('off')
table = ax2.table(cellText=performance_df.values, colLabels=performance_df.columns, rowLabels=['']*len(dates), cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(.8, .8)

# Display the plot
plt.show()
######################################################
###############################################################

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# Path to your graph image
image_path = '_returns_graph.png'  # Update this path to where your image is stored

# Your text message
#report_p1 = "This is a summary report of investment growth over time "

# Create a PDF using reportlab
pdf_filename = '_generated_report.pdf'  # Update the path as needed

c = canvas.Canvas(pdf_filename, pagesize=letter)
width, height = letter  # Get dimensions of the letter size

# Add the text at the top
c.setFont("Helvetica-Bold", 12)  # Using bold Helvetica font at size 14
text = c.beginText(20, height - 100)
text.setTextOrigin(20, height - 50)  # Set the start position of the text
text.textLines(report_p1)
c.drawText(text)

# Include the graph image
image = ImageReader(image_path)
image_width, image_height = image.getSize()
aspect_ratio = image_width / image_height
image_height = 400 / aspect_ratio  # Maintain aspect ratio based on a desired width of 400

# Draw the image centered on the page
c.drawImage(image, (width - 300) / 2, (height - 650) / 2, width=400, height=image_height, preserveAspectRatio=True)

# make sure the table dividend -> its accounting clearly 
# make that graph pretty clear -> labels and correct x and y axis  -> starts at 100k (just clarify )
# have a few testing for placing this in your laptop 
