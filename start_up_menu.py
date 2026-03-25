import record_expenses
import view_expenses

class Menu:
     '''Class representing the startup menu of the application.'''

     def __init__(self, file_record_expenses: str = 'record_expenses.py') -> None:
        '''Initializes the Menu object.
        :param : add_expenses, view_expenses'''

        self.file_record_expenses = file_record_expenses
        #self.view_expenses = view_expenses
    
     def display_menu(self):
        "Displays the menu options."

        print('-----------------------------------------------')
        print('💸 Welcome to the Monthly Expenses Tracker! 💸')
        print('-----------------------------------------------')
        while True:
            try:
                menu_options : dict = {
                    1: 'Add an expense',
                    2: 'View expenses',
                    #3: 'Edit an expense',
                    #4: 'Delete an expense',
                    #5: 'Statistics',
                    3: 'Exit'
                }
                for key, value in menu_options.items():
                    print(f"{key}: {value}")
                user_option : int = int(input('📆 Please select an option: '))
                if user_option == 1:
                    execute = record_expenses.MonthlyExpenses()
                    execute.user_input()
                elif user_option == 2:
                    view_expenses.view_menu()
                elif user_option not in menu_options.keys():
                    raise ValueError
                break
            except ValueError:
                print("Please enter a valid number.")

menu = Menu()
menu.display_menu()