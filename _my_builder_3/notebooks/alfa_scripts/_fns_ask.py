
def update_df_with_selections(df, stock_names):
    df['selected_stocks'] = None  # Initialize the new column for selected stocks
    
    # Use the stock names from the DataFrame for each row
    for index, row in df.iterrows():
        print(f"For the stock {row['Stock']}, you are selling = {row['PercentSold']}%")
        selected_stocks = stock_transaction(stock_names)
        # Store the selected stocks as a string representation of the list
        df.at[index, 'selected_stocks'] = selected_stocks ######################## change it was str(selected_stocks)
    
    return df
############################################################################
############################################################################

def allocate_percentages_to_stocks(df):
    df['allocation_percentages'] = None  # Initialize the new column for allocation percentages

    for index, row in df.iterrows():
        selected_stocks = eval(row['selected_stocks'])  # Assuming 'selected_stocks' is stored as a string representation of a list
        if not selected_stocks:  # Skip rows where no stocks were selected
            continue

        print(f"Allocating percentages for the following selected stocks: {', '.join(selected_stocks)}")
        allocation_percentages = []
        total_percentage_allocated = 0

        for i, stock in enumerate(selected_stocks, start=1):
            if i == len(selected_stocks) and total_percentage_allocated < 100:
                # Automatically allocate the remaining percentage to the last stock if not already 100%
                print(f"\n & % >> Automatically allocating the remaining {100 - total_percentage_allocated}% to {stock}.")
                allocation_percentages.append(100 - total_percentage_allocated)
                break

            while True:
                try:
                    user_input = input(f"\n % input >> Enter the percentage to allocate to {stock} (remaining {100 - total_percentage_allocated}%): ").strip()
                    percentage = int(user_input)
                    
                    if percentage <= 0 or percentage > 100 - total_percentage_allocated:
                        raise ValueError("Invalid percentage entered.")

                    allocation_percentages.append(percentage)
                    total_percentage_allocated += percentage
                    break  # Exit the while loop once a valid input is received
                except ValueError as e:
                    print("Please enter a valid percentage.")

        df.at[index, 'allocation_percentages'] = str(allocation_percentages)
    
    return df

############################################################################
############################################################################

############################################################################
############################################################################

# DO YOU WANT TO ADD any new ENTRIES ?
########################################## Add TRANS
def stock_transaction(stock_names):
    while True:
        print("Select a stock by number to indicate a SELL action, or press enter to exit:")
        for i, stock in enumerate(stock_names, start=1):
            print(f"{i}. {stock}")
        
        user_input = input("> ").strip()
        
        if not user_input:
            print("Exiting...")
            return None
        
        try:
            selection = int(user_input)
            if 1 <= selection <= len(stock_names):
                return stock_names[selection - 1]
            else:
                print("Invalid selection. Please choose a valid number.")
        except ValueError:
            print("Please enter a number or press enter to exit.")

############################################################################
############################################################################           
def handle_transaction(stock_name, df):

    if stock_name is None:
        print("No stock selected. Exiting...")
        return
    
    # Find the stock in the DataFrame
    if stock_name in df['Stock'].values:
        current_value = df.loc[df['Stock'] == stock_name, 'hold_units_at_init'].iloc[0]
        print(f"Current number of UNITS of {stock_name}: {current_value}")
        
        percent_sold = float(input("Enter the % amount to be sold (0-100): "))
        amount_sold = (percent_sold / 100) * current_value
        
        # Create a new DataFrame to export
        df_drop = pd.DataFrame({
            'Stock': [stock_name],
            'PercentSold': [percent_sold]
            
        })
        
        # Here you could save df_drop as a file or return it for further use
        return df_drop
    else:
        print("Stock not found in DataFrame.")
        return None

############################################################################
############################################################################
########################################## DATES


def input_date_and_confirm():
    # Dictionary mapping month inputs to their numerical representation
    month_mapping = {
        "jan": "01", "january": "01",
        "feb": "02", "february": "02",
        "mar": "03", "march": "03", "marz": "03",
        "apr": "04", "april": "04",
        "may": "05",
        "jun": "06", "june": "06",
        "jul": "07", "july": "07",
        "aug": "08", "august": "08",
        "sep": "09", "september": "09",
        "oct": "10", "october": "10",
        "nov": "11", "november": "11",
        "dec": "12", "december": "12"
    }

    while True:
        # Ask for user input
        month_input = input("Enter the month (e.g., Jan, February): ").lower()
        day_input = input("Enter the day (DD): ")
        year = input("Enter the year (YYYY): ")

        # Map the month input to its numerical representation
        month = month_mapping.get(month_input[:3], "Invalid")  # Default to "Invalid" if not found

        # Validate month
        if month == "Invalid":
            print("Invalid month entered. Please try again.")
            continue

        # Ensure day and month are correctly formatted with leading zeros if necessary
        day = f"{int(day_input):02d}"  # Convert to integer and format with leading zero if single digit
        month = f"{int(month):02d}"  # Ensure month is also correctly formatted (necessary if directly input as a number)

        # Format the date
        formatted_date = f"{year}-{month}-{day}"

        # Ask for confirmation
        confirm = input(f"Is this date correct? (Y/N) {formatted_date}: ").lower()
        
        # Check confirmation
        if confirm == 'y':
            print(f"Confirmed date (yyyy-mm-dd): {formatted_date}")
            return formatted_date
        else:
            print("Let's try again.")


############################################################################
############################################################################

def stock_transaction_exchange(stock_names):
    selected_stocks = []
    while True:
        print("\nE >>> Select stocks by typing their **number** or name to indicate a SELECTION,")
        print(" >>> IF EXCHANGE ::: type **CASH** if part of this SALE will go to straight to CASH:")
        print(" >>> type a **new stock** name to add it, or press enter to exit:\n")

        for i, stock in enumerate(stock_names, start=1):
            print(f"{i}. {stock}")

        user_inputs = input("> ").strip().upper().split(",")  # Allow multiple inputs separated by commas

        if not user_inputs or user_inputs == ['']:  # Check for exit condition
            if selected_stocks:
                print(f"\nExiting... You've selected the following stocks: {', '.join(selected_stocks)}")
            else:
                print("Exiting without any selection...")
                rsp_updt = 'n'
            break

        for user_input in user_inputs:
            user_input = user_input.strip()
            if user_input.isdigit():  # Select by number
                index = int(user_input)
                if 1 <= index <= len(stock_names):
                    selected_stock = stock_names[index - 1]
                    if selected_stock not in selected_stocks:
                        selected_stocks.append(selected_stock)
                else:
                    print(f"Invalid selection '{user_input}'. Please choose valid numbers or enter stock names.")
            else:  # Select by name or add new
                if user_input in stock_names:  # Already exists, select it
                    if user_input not in selected_stocks:
                        selected_stocks.append(user_input)
                elif user_input:  # New stock, add and select
                    stock_names.append(user_input)
                    selected_stocks.append(user_input)
                    print(f"New stock '{user_input}' added and selected.")

    return selected_stocks
    
############################################################################


def update_df_with_selections_exchange(df, stock_names):
    df['selected_stocks'] = None  # Initialize the new column for selected stocks

    # Use the stock names from the DataFrame for each row
    for index, row in df.iterrows():
        print(f"For the stock {row['Stock']}, you are selling = {row['PercentSold']}%")
        selected_stocks = stock_transaction_exchange(stock_names)
        # Store the selected stocks as a string representation of the list
        df.at[index, 'selected_stocks'] = str(selected_stocks)

    return df
############################################################################
############################################################################ CE



def allocate_percentages_to_stocks_ce(stock_names, trans_date):
    if not stock_names:
        print("The stock list is empty.")
        return

    # Asking for the total percentage of excess cash to allocate to stocks
    while True:
        try:
            total_cash_allocation = float(input("Enter the total percentage of your excess cash (up to 100) to allocate to stocks: "))
            if 0 <= total_cash_allocation <= 100:
                break
            else:
                print("Please enter a value between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    print(f"Total allocation available for stocks: {total_cash_allocation}% of your excess cash")

    total_allocation = 100
    allocations = []

    for stock in stock_names[:-1]:  # Loop through all but the last stock
        while True:
            try:
                print(f"Remaining allocation available: {total_allocation}%")
                allocation = float(input(f"Enter the allocation percentage for {stock} as a whole number: "))
                if allocation < 0:
                    print("Please enter a non-negative value.")
                elif allocation > total_allocation:
                    print(f"Allocation exceeds the remaining {total_allocation}% total. Try again.")
                else:
                    allocations.append(allocation)
                    total_allocation -= allocation
                    break
            except ValueError:
                print("Invalid input. Please enter a number.")
        
    # Automatically assign the remaining allocation to the last stock
    allocations.append(total_allocation)
    print(f"The allocation for {stock_names[-1]} has been automatically set to {total_allocation}%.")

    # Adjusting allocations based on the total percentage of excess cash designated for stocks
    adjusted_allocations = [alloc * total_cash_allocation / 100 for alloc in allocations]

    # Creating DataFrame with actual, adjusted allocations
    df_ce_start = pd.DataFrame({
        'date_cash_to_stock': [trans_date] * len(stock_names),
        'per_cash_to_stock': adjusted_allocations,  # Use the adjusted list of allocations
        'Stock': stock_names
    })
    
    return adjusted_allocations, df_ce_start







