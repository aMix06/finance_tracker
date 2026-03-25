import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

file_path = 'data.csv'
df = pd.read_csv(file_path)
df['Date'] = pd.to_datetime(df['Date'])
df_expenses = df.set_index('Date')
current_date = datetime.date.today()

def view_menu():
    while True:
        try:
            user_option : int = int(input("Would you like to see this week's or a particular month's expenses? (Week [1] or Month [0]) : "))
            if user_option == 1:
                display_weekly_expenses()
            elif user_option == 0:
                display_monthly_expenses()
            else:
                raise ValueError
            break
        except ValueError:
            print('Please enter a valid number.')

def display_weekly_expenses():
    current_week_day = current_date.weekday()

    start_week = current_date - datetime.timedelta(current_week_day)
    end_week = start_week + datetime.timedelta(6)

    start_ts = pd.Timestamp(start_week)
    end_ts = pd.Timestamp(end_week)

    df_week = df_expenses[(df_expenses.index >= start_ts) & (df_expenses.index <= end_ts)]

    total_week = df_week['Amount'].sum()
    week_by_category = df_week.groupby('Type of expense')['Amount'].sum()
    print(f'This week, you spent {total_week} EUR in total.')
    for category, amount in week_by_category.items():
        print(f'{category} : {amount} EUR')
        
    while True:
        try:
            user_option : int = int(input('Would you like to see in detail? (Yes [1] or No [0]) : '))
            if user_option == 1:
                print(df_week)
            elif user_option == 0:
                break
            else:
                raise ValueError
            break
        except ValueError:
            print('Please enter a valid number.')

def display_monthly_expenses():
    while True:
        try:
            month_choice: int = int(input('📆 Please enter the month (1-12): '))
            if month_choice < 1 or month_choice > 12:
                print('Please enter a valid month (1-12).')
                continue  # Ask for the month again if invalid
            elif month_choice > datetime.date.today().month:
                print('Only months up to the current month are accepted.')
                continue
            break  # Exit loop if valid month is entered
        except ValueError:
            print('Please enter a valid month (1-12).')

    df_month = df_expenses.loc[df_expenses.index.month == month_choice]
    total_month = df_month['Amount'].sum()
    month_by_category = df_month.groupby('Type of expense')['Amount'].sum()
    print(f'This month, you spent {total_month} EUR in total.')
    for category, amount in month_by_category.items():
        print(f'{category} : {amount} EUR')
    
        
    while True:
        try:
            user_option : int = int(input('Would you like to see in detail? (Yes [1] or No [0]) : '))
            if user_option == 1:
                print(df_month)
            elif user_option == 0:
                break
            else:
                raise ValueError
            break
        except ValueError:
            print('Please enter a valid number.')