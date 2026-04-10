#-------------------------------#
#           LIBRARIES
#-------------------------------#
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import json
from typing import Dict, Tuple, List

# OLLAMA API
import ollama

#-------------------------------#
#    INITIALIZING DATAFRAME
#-------------------------------#
def initialization() -> None:
    print('-----------------------------------------------')
    print('💸 Welcome to the Monthly Expenses Tracker! 💸')
    print('-----------------------------------------------')

    while True:
        file_path = input("Paste the statement file name here: ")
        try:
            data = pd.read_csv(file_path, encoding='utf-8')
            print("✓ File loaded successfully!")
            break
        except FileNotFoundError:
            print("✗ File not found. Please check the path.")
        except pd.errors.EmptyDataError:
            print("✗ The CSV file is empty.")
        except pd.errors.ParserError:
            print("✗ Invalid CSV format.")
        except Exception as e:
            print(f"✗ Error: {e}")

    try:
        # EXPENSE CATEGORIES DATA
        categories_dict = 'categories.json'
        with open(categories_dict, 'r', encoding='utf-8') as d:
            dict_cat = json.load(d)
    except FileNotFoundError:
        dict_cat = {}
        with open(categories_dict, 'w', encoding='utf-8') as d:
            json.dump(dict_cat, d, indent=4)

    data = pd.read_csv(file_path, encoding='utf-8')
    data['Completed Date'] = pd.to_datetime(data['Completed Date'])
    df = data[['Type', 
            'Product', 
            'Completed Date', 
            'Description', 
            'Amount', 
            'Currency', 
            'Balance']].set_index('Completed Date')
    df.index = df.index.normalize()

    # DATAFRAME OF EXPENSES
    df_expenses = df[
        (df['Amount'] < 0) &
        (
            (df['Type'].isin(['Card Payment', 'Fee'])) |
            (
                (df['Type'] == 'Transfer') &
                ~(df['Description'].str.contains('Savings', case=False, na=False))
            )
        )
        ].copy()

    first_day_month, last_day_month = initializing_dates(df)
    
    main(df, df_expenses, first_day_month, last_day_month, dict_cat, categories_dict)

#--------------------------#
#    INITIALIZING DATES
#--------------------------#
def initializing_dates(df):
    first_day_month = df.index[0].date().replace(day=1)

    if (df.index.month == 12).any():
        next_month = first_day_month.replace(year=first_day_month.year + 1, month=1, day=1)
    else:
        next_month = first_day_month.replace(month=first_day_month.month + 1, day=1)
    last_day_month = next_month - datetime.timedelta(1)
    return first_day_month, last_day_month

#-----------------#
#    FUNCTIONS
#-----------------#
def main(df, df_expenses, first_day_month, last_day_month, dict_cat, categories_dict) -> None:
    "Main function."
    df_expenses['Category'] = df_expenses['Description'].apply(lambda desc : categorize_expense(desc, dict_cat, categories_dict))                      # STEP 1 : Categorizes each expense. Creates the "Category" column in the df_expenses.
    week_dict = separate_weeks(first_day_month, last_day_month)                                         # STEP 2 : Seperate the bank statement into weeks.
    while True:
        try:
            choice: int = int(input("Select a Monthly (0) or Weekly (1) analysis : "))
            if choice == 0:
                main_month(df,df_expenses, week_dict)
            elif choice == 1:
                main_week(df, df_expenses, week_dict)
            else:
                print("Invalid choice. Please enter 0 or 1.")
            break
        except ValueError:
            print("Please enter a valid number.")

def main_month(df, df_expenses, week_dict) -> None:
    """Main function for month analysis."""
    total_spent = round(abs(df_expenses['Amount'].sum()), 2)
    weekly_totals = {}
    for week in week_dict:
        start = week_dict[week][0]                                                         
        end   = week_dict[week][1]
        #mask = (df.index >= pd.Timestamp(start)) & (df.index <= pd.Timestamp(end))                          
        mask_exp = (df_expenses.index >= pd.Timestamp(start)) & (df_expenses.index <= pd.Timestamp(end))
        df_exp_week = df_expenses[mask_exp]
        spendings = round(abs(df_exp_week['Amount'].sum()), 2)
        weekly_totals[week] = spendings
    week_avg = sum(weekly_totals.values())/len(weekly_totals) if weekly_totals else 0
    initial_balance = df.iloc[0]['Balance']  
    ending_balance = df.iloc[-1]['Balance']
    display_month_summary(df_expenses, weekly_totals, total_spent, week_avg, initial_balance, ending_balance)
    month_vis(df_expenses)

def display_month_summary(df_expenses, weekly_totals, total_spent, week_avg, initial_balance, ending_balance):
    """Displays the summary of the month."""
    print(f'Inital balance : {initial_balance}')
    print(f'Ending balance : {ending_balance}')
    print(f'Total spent this month : {total_spent}')
    for w, val in weekly_totals.items():
        print(f'        {w:<10} : {val:.2f}')
    print(f'On average, you spend {week_avg} EUR each week.')
    for c in df_expenses['Category'].unique():
        print(f'        {c:<10} : {abs(df_expenses[df_expenses['Category'] == c]['Amount'].sum()):.2f}')

def month_vis(df_expenses) -> None:    
    '''Visualizes the expenses of a given month by category.'''
    d_pie = df_expenses.groupby('Category')['Amount'].sum().abs()
    
    fig, ax = plt.subplots()
    ax.pie(d_pie.values, labels=d_pie.index, autopct='%1.1f%%')
    ax.set_title('Expenses by Category')   

    plt.show()

def main_week(df, df_expenses, week_dict) -> None:
    """Main function for week analysis."""
    user_option = week_input(week_dict)                                                                 # STEP 3 : Prompts the user to select a week.
    start = week_dict[f'Week {user_option}'][0]                                                         # STEP 4 : Define the start and end of the selected week.
    end   = week_dict[f'Week {user_option}'][1]
    mask = (df.index >= pd.Timestamp(start)) & (df.index <= pd.Timestamp(end))                          # STEP 5 : Creates a mask of that week.
    mask_exp = (df_expenses.index >= pd.Timestamp(start)) & (df_expenses.index <= pd.Timestamp(end))    # STEP 6 : Create a mask of that week with expenses only.

    df_exp_week = df_expenses[mask_exp]                                                                 # STEP 7 : Define the df of that week with expenses only.
    df_summary = df_exp_week.groupby(df_exp_week.index.date)['Amount'].sum()                            # STEP 8 : Define the df for total spending per day.
    summary = week_summary(mask, df_summary, df_exp_week, df)                                           # STEP 9 : Outputs the week summary.
    display_week_summary(user_option, summary, df_exp_week, df_summary)
    week_vis(df_exp_week)

# CATEGORIZATION OF EXPENSES
def categorize_expense(description: str, dict_cat: dict, categories_dict: str) -> str:
    '''Returns the category of expense based on the description.'''
    
    # 1. Check patterns first (fastest)
    if description.lower().startswith("transfer to") or description.lower().startswith("to "):
        return "Transfers"
    
    # 2. Normalize the description
    normalized = normalize_description(description)
    
    # 3. Check if normalized version is cached
    if normalized in dict_cat:
        return dict_cat[normalized]["Category"]
    
    # 4. Not in cache - call LLM (slowest, last resort)
    category = llm_categorize(description)
    dict_cat[normalized] = {
        "Description": description,  # Store original for reference
        "Category": category
    }
    with open(categories_dict, 'w', encoding='utf-8') as file:
        json.dump(dict_cat, file, indent=4)
    
    return category 

def normalize_description(description: str) -> str:
    # Lowercase everything
    desc = description.lower()
    # Remove common prefixes
    desc = desc.replace("to ", "").replace("from ", "")
    # Remove extra spaces
    desc = " ".join(desc.split())
    return desc

def llm_categorize(description: str) -> str:
    '''Returns the category of an expense using LLM.'''
    # Initialize client
    client = ollama.Client()
    
    model = 'deepseek-r1:8b'

    # Define your actual prompt
    prompt = f"""
    Associate this expense description "{description}"
    with one of these categories ONLY:
    "Transfers", "Services", "Travel", "Transportation",
    "Restaurants", "Groceries", "Entertainment", "Shopping",
    "Withdrawal". Categorize expense "Other" if you are unable to associate it to any previous categories.
    Only respond with the category name (ONE WORD).
    """

    # Generate response
    response = client.generate(model=model, prompt=prompt)

    category = response['response'].strip()

    # Extract text safely
    return category

# DISPLAY EXPENSES
def separate_weeks(first_day_month, last_day_month) -> Dict[str, List]:
    '''Separates the month into weeks and 
    returns a dictionary with each week as a key and the corresponding start and end dates as values.'''
    #First week
    week_start = first_day_month
    i = 0
    week_dict = {}

    while week_start <= last_day_month:
        week_end = week_start + datetime.timedelta(6 - week_start.weekday())
        if week_end > last_day_month:
            week_end = last_day_month

        week_dict[f'Week {i}'] = [week_start, week_end]

        week_start = week_end + datetime.timedelta(1)
        i += 1
    return week_dict

def week_input(week_dict: Dict[str, List]) -> int:
    '''Prompts the user to select a week and returns the week number.'''
    menu_options = {i : week for i, week in enumerate(week_dict)}
    while True:
        try:
            print("Select a week to view your finances :")
            for key, value in menu_options.items():
                print(f"{key}: {value}")
            user_option : int = int(input('Week '))
            if user_option not in menu_options.keys():
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid number.")
    
    return user_option

def week_summary(mask, df_summary, df_exp_week, df) -> Dict[str, float]:
    '''Returns a dictionary with the summary of the week.'''
    summary = {}

    spendings = round(abs(df_exp_week['Amount'].sum()), 2)
    earnings = round(df.loc[mask][df.loc[mask]['Amount'] > 0]['Amount'].sum(), 2)
    balance = round((earnings - spendings), 2)
    highest_spending = abs(df_summary.min())
    most_frequent_spending = df_exp_week['Category'].value_counts().idxmax()
    frequency = df_exp_week['Category'].value_counts().max()

    biggest_expense = df_exp_week.loc[df_exp_week['Amount'] == df_exp_week['Amount'].min()]
    amount = abs(biggest_expense['Amount'].iloc[0]) 
    description = biggest_expense['Description'].iloc[0]
    category = biggest_expense['Category'].iloc[0]
    date = biggest_expense.index[0].date()
    
    summary['spendings'] = spendings
    summary['earnings'] = earnings
    summary['balance'] = balance
    summary['highest spending'] = highest_spending
    summary['most frequent spending'] = (most_frequent_spending, frequency)
    summary['biggest_expense'] = (amount, description, category, date)

    return summary

def display_week_summary(user_option, summary, df_exp_week, df_summary) -> None:
    '''Displays a summary of the expenses for a given week.'''
    print('---------------------------')
    print(f'    Overview of week {user_option}')
    print('---------------------------')
    
    print(f'Spent : {summary['spendings']} EUR')
    for c in df_exp_week['Category'].unique():
        print(f'        {c:<10} : {abs(df_exp_week[df_exp_week['Category'] == c]['Amount'].sum())}')
    print(f'Earned : {summary['earnings']} EUR')
    print(f'Net balance : {summary['balance']} EUR')
    
    print(f'Highest spending day was on the {df_summary.idxmin()} with the amount being {summary['highest spending']:.2f} EUR.')
    print(f'Most frequent spending category is {summary['most frequent spending'][0]} ({summary['most frequent spending'][1]} times)')
    print(f'The biggest expense this week was €{summary['biggest_expense'][0]}, spent on {summary['biggest_expense'][1]} ({summary['biggest_expense'][2]}), on {summary['biggest_expense'][3]}.')

def week_vis(df_exp_week) -> None:    
    
    '''Visualizes the expenses of a given week by category.'''
    d_pie = df_exp_week.groupby('Category')['Amount'].sum().abs()
    
    fig, ax = plt.subplots()
    ax.pie(d_pie.values, labels=d_pie.index, autopct='%1.1f%%')
    ax.set_title('Expenses by Category')   

    plt.show()

if __name__ == "__main__":
    initialization()