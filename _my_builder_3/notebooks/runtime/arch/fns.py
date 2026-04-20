

# # def calculate_investment_details(start_dates_list, stock_symbol, investment_amount):
# #     import yfinance as yf
# #     from datetime import datetime
# #     """
# #     Calculate the investment details, including the initial and current stock prices,
# #     the current value of the investment, and the percentage change.

# #     Parameters:
# #     - start_date_str: Start date for the investment in the format 'YYYY-MM-DD'
# #     - stock_symbol: Symbol of the stock (e.g., 'AAPL' for Apple Inc.)
# #     - investment_amount: Amount of money invested

# #     Returns:
# #     - Initial stock price, latest stock price, current value of the investment, and the percentage change.
# #     """
# #     # Convert start date string to datetime object
# #     results = [] # Initialize an empty list to store results for each start date

# #     for start_date_str in start_dates_list:
# #         # Convert start date string to datetime object
# #         start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

# #         # Fetch stock data from Yahoo Finance for the specified period
# #         stock_data = yf.download(stock_symbol, start=start_date_str)

# #         if stock_data.empty:
# #             results.append(("Stock data is unavailable. Please check the stock symbol and start date.",))
# #             continue

# #         try:
# #             # Get the closing price of the stock on the start date
# #             start_price = stock_data.iloc[0]['Close']
# #         except IndexError:
# #             results.append(("The start date may be a non-trading day. Please adjust the date.",))
# #             continue

# #         # Fetch the most recent stock data
# #         latest_price = stock_data.iloc[-1]['Close']

# #         # Calculate the current value of the investment
# #         current_value = (latest_price / start_price) * investment_amount
# #         percentage_change = ((latest_price - start_price) / start_price) * 100

# #         # Append the details for this start date to the results list
# #         results.append((start_price, latest_price, current_value, percentage_change))

# #     return results
# # def calculate_investment_details(start_date_str, stock_symbol, investment_amount):
# #     import yfinance as yf
# #     from datetime import datetime
# #     """
# #     Calculate the investment details, including the initial and current stock prices,
# #     the current value of the investment, and the percentage change.

# #     Parameters:
# #     - start_date_str: Start date for the investment in the format 'YYYY-MM-DD'
# #     - stock_symbol: Symbol of the stock (e.g., 'AAPL' for Apple Inc.)
# #     - investment_amount: Amount of money invested

# #     Returns:
# #     - Initial stock price, latest stock price, current value of the investment, and the percentage change.
# #     """
# #     # Convert start date string to datetime object
# #     start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

# #     # Fetch stock data from Yahoo Finance
# #     stock_data = yf.download(stock_symbol, start=start_date_str)

# #     if stock_data.empty:
# #         return "Stock data is unavailable. Please check the stock symbol and start date."

# #     # Get the closing price of the stock on the start date
# #     try:
# #         start_price = stock_data.iloc[0]['Close']
# #     except IndexError:
# #         return "The start date may be a non-trading day. Please adjust the date."

# #     # Fetch the most recent stock data
# #     latest_price = stock_data.iloc[-1]['Close']

# #     # Calculate the current value of the investment
# #     current_value = (latest_price / start_price) * investment_amount
# #     percentage_change = ((latest_price - start_price) / start_price) * 100

# #     return start_price, latest_price, current_value, percentage_change

# ########################################## Add TRANS
# def stock_transaction(stock_names):
#     while True:
#         print("Select a stock by number to indicate a SELL action, or press enter to exit:")
#         for i, stock in enumerate(stock_names, start=1):
#             print(f"{i}. {stock}")
        
#         user_input = input("> ").strip()
        
#         if not user_input:
#             print("Exiting...")
#             return None
        
#         try:
#             selection = int(user_input)
#             if 1 <= selection <= len(stock_names):
#                 return stock_names[selection - 1]
#             else:
#                 print("Invalid selection. Please choose a valid number.")
#         except ValueError:
#             print("Please enter a number or press enter to exit.")

# ################            
# def handle_transaction(stock_name, df):
#     import pandas as pd

#     if stock_name is None:
#         print("No stock selected. Exiting...")
#         return
    
#     # Find the stock in the DataFrame
#     if stock_name in df['Stock'].values:
#         current_value = df.loc[df['Stock'] == stock_name, 'hold_units_at_init'].iloc[0]
#         print(f"Current number of UNITS of {stock_name}: {current_value}")
        
#         percent_sold = float(input("Enter the % amount to be sold (0-100): "))
#         amount_sold = (percent_sold / 100) * current_value
        
#         # Create a new DataFrame to export
#         df_drop = pd.DataFrame({
#             'Stock': [stock_name],
#             'PercentSold': [percent_sold]
            
#         })
        
#         # Here you could save df_drop as a file or return it for further use
#         return df_drop
#     else:
#         print("Stock not found in DataFrame.")
#         return None


# ########################################## DATES




# def input_date_and_confirm():
#     # Dictionary mapping month inputs to their numerical representation
#     month_mapping = {
#         "jan": "01", "january": "01",
#         "feb": "02", "february": "02",
#         "mar": "03", "march": "03", "marz": "03",
#         "apr": "04", "april": "04",
#         "may": "05",
#         "jun": "06", "june": "06",
#         "jul": "07", "july": "07",
#         "aug": "08", "august": "08",
#         "sep": "09", "september": "09",
#         "oct": "10", "october": "10",
#         "nov": "11", "november": "11",
#         "dec": "12", "december": "12"
#     }

#     while True:
#         # Ask for user input
#         month_input = input("Enter the month (e.g., Jan, February): ").lower()
#         day_input = input("Enter the day (DD): ")
#         year = input("Enter the year (YYYY): ")

#         # Map the month input to its numerical representation
#         month = month_mapping.get(month_input[:3], "Invalid")  # Default to "Invalid" if not found

#         # Validate month
#         if month == "Invalid":
#             print("Invalid month entered. Please try again.")
#             continue

#         # Ensure day and month are correctly formatted with leading zeros if necessary
#         day = f"{int(day_input):02d}"  # Convert to integer and format with leading zero if single digit
#         month = f"{int(month):02d}"  # Ensure month is also correctly formatted (necessary if directly input as a number)

#         # Format the date
#         formatted_date = f"{year}-{month}-{day}"

#         # Ask for confirmation
#         confirm = input(f"Is this date correct? (Y/N) {formatted_date}: ").lower()
        
#         # Check confirmation
#         if confirm == 'y':
#             print(f"Confirmed date (yyyy-mm-dd): {formatted_date}")
#             return formatted_date
#         else:
#             print("Let's try again.")



