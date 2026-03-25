import csv

data = "data.csv"
f = open(data, "w")
f.truncate()
f.close()

column_names = ['Date', 'Amount', 'Currency', 'Type of payment', 'Type of expense', 'Description', 'Location', 'Date of register']
with open(data, 'a', newline='') as csvfile:
    expense_writer = csv.DictWriter(csvfile, fieldnames=column_names)
    if csvfile.tell() == 0: 
        expense_writer.writeheader()