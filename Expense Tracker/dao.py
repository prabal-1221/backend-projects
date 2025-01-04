from models import Expense
import pandas as pd

PATH = 'database.txt'

def write_expense(expense):
    with open(PATH, 'a') as f:
        f.write(str(expense)+'\n')

def read_expense():
    with open(PATH, 'r') as f:
        texts = []
        for line in f.readlines():
            texts.append(line)
    
    return texts

class ExpenseDao:
    def add_expense(description, amount):
        new_expense = Expense(description, amount)
        write_expense(new_expense)
    
    def print_expenses():
        data = read_expense()

        for line in data:
            print("{: <5} {: <15} {: <30} {: <10}".format(*line.split(',')))
    
    def summary_expense():
        data = read_expense()

        total_amount = 0
        for line in data[1:]:
            _, _, _, amount = line.split(',')
            total_amount += int(amount)
        
        print(total_amount)
    
    def delete_expense(delete_id):
        data = read_expense()
        with open(PATH, 'w') as f:
            f.write('id,date,description,amount\n')

        for line in data[1:]:
            id, date, description, amount = line.split(',')
            if int(id) == delete_id:
                continue
            expense = Expense(description, int(amount), id, date)
            write_expense(expense)
        
    def summary_expense_month(month):
        data = read_expense()

        total_amount = 0
        for line in data[1:]:
            _, date, _, amount = line.split(',')
            if int(date[5:7]) == int(month):
                total_amount += int(amount)
        
        print(total_amount)
    
    def update_expense(update_id, update_description, update_amount):
        data = read_expense()
        with open(PATH, 'w') as f:
            f.write('id,date,description,amount\n')

        for line in data[1:]:
            id, date, description, amount = line.split(',')
            new_description = description
            new_amount = int(amount)
            if int(id) == update_id:
                new_description = update_description
                new_amount = int(update_amount)
            
            expense = Expense(new_description, new_amount, id, date)
            write_expense(expense)
    
    def export_expenses():
        df = pd.read_csv(PATH)
        df.to_csv('expenses.csv', index=None)