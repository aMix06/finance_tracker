from typing import Any, List, Tuple, Dict
import csv
import statistics
import datetime
from collections import defaultdict
import pandas as pd
from decimal import Decimal

class Expense:
    '''Class representing an expense.'''
    
    def __init__(self, date: str, amount: float, currency: str, payment_type: str, expense_type: str, description: str, location: str, date_register: str) -> None:
        '''Initializes the Expense object.
        :param : date, currency, amount, payment_type, expense_type, description, location, date of register'''
        self.date = date
        self.amount = amount
        self.currency = currency
        self.payment_type = payment_type
        self.expense_type = expense_type
        self.description = description
        self.location = location
        self.date_register = date_register
    
    def __str__(self): 
        '''Returns a string representation of the Expense object.'''
        if self.currency == "VND":
            return f'✅ On {self.date}, you spent {format(self.amount, ",")} {self.currency} on {self.description} ({self.expense_type}) at {self.location} using {self.payment_type} [REGISTERED ON {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}].'
        else:
            return f'✅ On {self.date}, you spent {self.amount} {self.currency} on {self.description} ({self.expense_type}) at {self.location} using {self.payment_type} [REGISTERED ON {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}].'

    def convert_to_dict(self) -> Dict[str, Any]:
        '''Converts the Expense object parameters into a dictionary.'''
        return {
            'Date': self.date,
            'Amount': self.amount,
            'Currency': self.currency,
            'Type of payment': self.payment_type,
            'Type of expense': self.expense_type,
            'Description': self.description,
            'Location': self.location,
            'Date of register': self.date_register
        }

class MonthlyExpenses:
    '''Class representing an expense of a particular month.'''

    def __init__(self, file_path: str = 'data.csv'):
        '''Initializes the MonthlyExpenses object.'''
        self.data: List[Dict[str, Any]] = []
        self.file_path = file_path

    def user_input(self) -> None:
        '''Generates user inputs'''
        
        #while True: 
        #    try:
        #        year: int = int(input('Please enter the year: '))
        #        if year != datetime.date.today().year:
        #            print('Only the current year is accepted.')
        #            continue  # Ask for the year again if invalid
        #        break  # Exit loop if valid year is entered
        #    except ValueError:
        #        print('Please enter a valid year.')

        date_register = datetime.date.today()
        print(f'Today is: {date_register}')
        print("*Note : Only payments of the current year are accepted.*")
        print('--------------------------------------------------------')
        year = datetime.date.today().year        

        while True:
            try:
                month: int = int(input('📆 Please enter the month (1-12): '))
                if month < 1 or month > 12:
                    print('Please enter a valid month (1-12).')
                    continue  # Ask for the month again if invalid
                elif month > datetime.date.today().month:
                    print('Only months up to the current month are accepted.')
                    continue
                break  # Exit loop if valid month is entered
            except ValueError:
                print('Please enter a valid month (1-12).')

        while True:
            try:
                day: int = int(input('📆 Please enter the day (1-31): '))
                if day < 1 or day > 31:
                    print('Please enter a valid day (1-31).')
                    continue  # Ask for the day again if invalid
                elif month == datetime.date.today().month and day > datetime.date.today().day:
                    print('Only days up to the current day are accepted.')
                    continue
                expense_date = datetime.date(year, month, day)
                break  # Exit loop if valid day is entered and date is valid
            except ValueError:
                print('Please enter a valid day (1-31).')
            except Exception:
                print('Please enter a valid date.')
        
        while True: 
            try: 
                num_currency: int = int(input('💱 Please enter the currency by entering number (EUR [1] or VND [2]): '))
                if num_currency == 1:
                    currency = "EUR"
                elif num_currency == 2:
                    currency = "VND"
                if type(num_currency) != int:
                    raise ValueError
                elif num_currency < 1 or num_currency > 2:
                    raise ValueError
                break
            except ValueError:  
                print('Please enter a valid currency.')

        while True:
            try:
                if currency == "VND":
                    amount: Decimal = Decimal(input('💰 Please enter the amount (in thousands): ')) * 1000
                    if amount <= 0:
                        raise ValueError
                elif currency == "EUR":
                    amount: Decimal = Decimal(input('💰 Please enter the amount (in euros): '))
                    if amount <= 0:
                        raise ValueError
                break
            except ValueError:
                print('Please enter a valid amount.')

        while True: 
            try: 
                num_payment_type: int = int(input('Please enter the type of payment by entering number (💳 Card [1] or 💵 Cash [2]): '))
                if num_payment_type == 1:
                    payment_type = "Card"
                elif num_payment_type == 2:
                    payment_type = "Cash"
                if type(num_payment_type) != int:
                    raise ValueError
                elif num_payment_type < 1 or num_payment_type > 2:
                    raise ValueError
                break
            except ValueError:  
                print('Please enter a valid payment type.')

        while True: 
            try: 
                l = ["1.Transfers 📩", 
                     "2.Services 🏬", 
                     "3.Travel ✈️", 
                     "4.Transportation 🚖", 
                     "5.Restaurants 🍽️", 
                     "6.Groceries 🛒", 
                     "7.Entertainment 🎉", 
                     "8.Shopping 🛍️", 
                     "9.Withdrawal 🏧"]
                for category in l:
                    print(category)
                num_expense_type: int = int(input('Please choose the type of expense by entering a number: '))
                if num_expense_type == 1:
                    expense_type = "Transfers"
                elif num_expense_type == 2:
                    expense_type = "Services"
                elif num_expense_type == 3:
                    expense_type = "Travel"
                elif num_expense_type == 4:
                    expense_type = "Transportation"
                elif num_expense_type == 5:
                    expense_type = "Restaurants"
                elif num_expense_type == 6:
                    expense_type = "Groceries"
                elif num_expense_type == 7:
                    expense_type = "Entertainment"
                elif num_expense_type == 8:
                    expense_type = "Shopping"
                elif num_expense_type == 9:
                    expense_type = "Withdrawal"
                if type(num_expense_type) != int:
                    raise ValueError
                elif num_expense_type < 1 or num_expense_type > 9:
                    raise ValueError
                break
            except ValueError:  
                print('Please enter a valid expense type.')
        
        while True: 
            try: 
                description: str = input('📝 Please enter a description (what was purchased): ').strip()
                if type(description) != str:
                    raise ValueError
                break
            except ValueError:  
                print('Please enter a valid description.')

        while True: 
            try: 
                location: str = input('📍 Please enter the location (from where the purchase was made): ').strip()
                if type(location) != str:
                    raise ValueError
                break
            except ValueError:  
                print('Please enter a valid location.')

        expense: Expense = Expense(expense_date, amount, currency, payment_type, expense_type, description, location, date_register)
        self.data.append(expense.convert_to_dict())
        print(expense)
        self.write_csv()
        self.sort_row()

    def sort_row(self):
        """Sorts the data by date."""
        df = pd.read_csv(self.file_path)
        sorted_df_by_date = df.sort_values(by='Date', ascending=False)
        sorted_df_by_date.to_csv(self.file_path, index=False)

    def write_csv(self):
        """
        Writes the data to a CSV file.
        This method opens the CSV file specified by the `file_path` attribute, appends the data to it, and writes the column names if the file is empty. The data is stored in a list of dictionaries, where each dictionary represents an expense and contains keys for the column names. After writing the data, the list is cleared.
        """
        column_names = ['Date', 'Amount', 'Currency', 'Type of payment', 'Type of expense', 'Description', 'Location', 'Date of register']
        with open(self.file_path, 'a', newline='') as csvfile:
            expense_writer = csv.DictWriter(csvfile, fieldnames=column_names)
            if csvfile.tell() == 0: 
                expense_writer.writeheader()
            expense_writer.writerows(self.data)
        self.data = []

#    def perform_eda(self):

#tracker = MonthlyExpenses()
#tracker.record_expense()


    