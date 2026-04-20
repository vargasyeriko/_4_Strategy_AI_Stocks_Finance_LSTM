

############################################################################
############################################################################
import pandas as pd

def stock_transaction(stock_names):
    selected_stocks = []

    while True:
        print("Select stocks by number to indicate a SELL action (e.g., '1, 3, 5'), or press enter to exit:")
        for i, stock in enumerate(stock_names, start=1):
            print(f"{i}. {stock}")

        user_input = input("> ").strip()

        if not user_input:
            if selected_stocks:
                print(f"Exiting... You've selected the following stocks: {', '.join(selected_stocks)}")
            else:
                print("Exiting without any selection...")
            break

        selections = [s.strip() for s in user_input.split(",") if s.strip()]

        for selection in selections:
            try:
                selection_index = int(selection)
                if 1 <= selection_index <= len(stock_names):
                    selected_stock = stock_names[selection_index - 1]
                    if selected_stock not in selected_stocks:  # Avoid adding duplicates
                        selected_stocks.append(selected_stock)
                else:
                    print(f"Invalid selection '{selection}'. Please choose valid numbers.")
            except ValueError:
                print(f"Please enter numbers or press enter to exit. '{selection}' is not a valid number.")

    return selected_stocks

def update_df_with_selections(df, stock_names):
    df['selected_stocks'] = None  # Initialize the new column for selected stocks
    
    # Use the stock names from the DataFrame for each row
    for index, row in df.iterrows():
        print(f"For the stock {row['Stock']}, you are selling = {row['PercentSold']}%")
        selected_stocks = stock_transaction(stock_names)
        # Store the selected stocks as a string representation of the list
        df.at[index, 'selected_stocks'] = selected_stocks ######################## change it was str(selected_stocks)
    
    return df




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

############################################################################
############################################################################

############################################################################
############################################################################

############################################################################
############################################################################

############################################################################
############################################################################

############################################################################
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

################            
def handle_transaction(stock_name, df):
    import pandas as pd

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
from datetime import datetime

#Get the current date and time ---------------------- ADD LOOP 


now = datetime.now()

# Format the date and time as requested: yyyy_mm_dd_hh
formatted_date_time = now.strftime("%Y_%m_%d_h%Hm%M")
import pandas as pd

#df= pd.read_pickle(f'_1_tables/_2_up_to_date_df0m_.pkl')


# GET PERCENT SOLD 

stock_names  = df['Stock']#.tolist()[:-2] 
selected_stock = stock_transaction(stock_names)
df_drop = handle_transaction(selected_stock, df)

# GET DATE

trans_date = input_date_and_confirm()
print("Your entered date is:", trans_date)

# ARRANGE TABLE -> new row entry
df_drop['keep_drop'] = 'd'
df_drop['trans_type'] = 's'
df_drop['DateTrans'] =trans_date 

##### 
rsp_updt = 'd'

# SHOW TABLE\
print('\n\n TABLE \n\n ')
import pandas as pd
def stock_transaction(stock_names):
    selected_stocks = []
    while True:
        print("\nE >>> Select stocks by typing their **number** or name to indicate a SELL action,")
        print(" >>> type **CASH** if part of this SALE will go to straight to CASH:")
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


def update_df_with_selections(df, stock_names):
    df['selected_stocks'] = None  # Initialize the new column for selected stocks

    # Use the stock names from the DataFrame for each row
    for index, row in df.iterrows():
        print(f"For the stock {row['Stock']}, you are selling = {row['PercentSold']}%")
        selected_stocks = stock_transaction(stock_names)
        # Store the selected stocks as a string representation of the list
        df.at[index, 'selected_stocks'] = str(selected_stocks)

    return df


## IF NO SELECTION
if rsp_updt != 'n':


    update_df_with_selections(df_drop,stock_names)
    # and contains a 'selected_stocks' column filled with selected stock names.===========================
    df_drop = allocate_percentages_to_stocks(df_drop)

    import ast

    # Assuming df is your DataFrame
    # Convert the string representation of a list to an actual list
    df_drop['selected_stocks'] = df_drop['selected_stocks'].apply(ast.literal_eval)
    # RENAME VARIABLES

    # Assuming 'df' is your DataFrame
    df_drop.rename(columns={'selected_stocks': 'exchange_stocks', 'allocation_percentages': 'sell_perc'}, inplace=True)

    df_drop['id_time'] = df_drop['Stock'] + "_" + df_drop['DateTrans'] + "_" + df_drop['trans_type']
    df_drop['DateTrans'] = pd.to_datetime(df_drop['DateTrans'])
    df_drop['DateTrans'] = df_drop['DateTrans'].dt.strftime('%Y-%m-%d')

    stock_new = df_drop.iloc[0,0][0:2]
    transtype_new = df_drop.iloc[0,4]
    print(f' \n\n  {df_drop}')
    print('\n\n ATTN : Are you sure you want to write this new entry to the tables_add?')
    rsp_updt = input('\n  ... y ... TO WRITE to tables and RUN updates  << or >> PRESS ENTER to EXIT \n\n')

    print(' *\n*\n* ')
    if rsp_updt == 'y':
        df_drop.to_pickle(f'_2_tables_add/_{stock_new}_{transtype_new}_type_HistAddNew_on_{formatted_date_time}.pkl')
        #    HISTORY
        print(f'\n*\n* ADDED !!! \n\n')

    else :
        print('EXITING ... \n\n')



############################################################################
############################################################################
# df and df_add to do the whole stock accomodation 
#df_add['DateTrans'] = df_add['DateTrans'].dt.strftime('%Y-%m-%d')

############################################################################
############################################################################

############################################################################
############################################################################

############################################################################
############################################################################




############################################################################
############################################################################

############################################################################
############################################################################

############################################################################
############################################################################

############################################################################
############################################################################




############################################################################
############################################################################

############################################################################
############################################################################

############################################################################
############################################################################

############################################################################
############################################################################


