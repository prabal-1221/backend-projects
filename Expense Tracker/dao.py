from models import Expense
import pandas as pd

PATH = 'database.txt'

def write_expense(description, amount):
    new_expense = Expense(description, amount)

    with open(PATH, 'a') as f:
        f.write(str(new_expense)+'\n')

def read_expense():
    with open(PATH, 'r') as f:
        texts = []
        for line in f.readlines():
            texts.append(line)
    
    return texts

def write_expense(id, date, description, amount):
    text = id + ',' + date + ',' + description + ',' + amount
    with open(PATH, 'a') as f:
        f.write(text)

class ExpenseDao:
    def add_expense(description, amount):
        write_expense(description, amount)
    
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
    
    def delete_expense(d_id):
        data = read_expense()
        with open(PATH, 'w') as f:
            f.write('id,date,description,amount\n')

        for line in data[1:]:
            id, date, description, amount = line.split(',')
            if id == d_id:
                continue
            write_expense(id, date, description, amount)
        
    def summary_expense_month(month):
        data = read_expense()

        total_amount = 0
        for line in data[1:]:
            _, date, _, amount = line.split(',')
            if int(date[5:7]) == int(month):
                total_amount += int(amount)
        
        print(total_amount)
    
    def update_expense(u_id, u_description, u_amount):
        data = read_expense()
        with open(PATH, 'w') as f:
            f.write('id,date,description,amount\n')

        for line in data[1:]:
            id, date, description, amount = line.split(',')
            if id == u_id:
                write_expense(id, date, u_description, str(u_amount)+'\n')
            else:
                write_expense(id, date, description, amount)
    
    def export_expenses():
        df = pd.read_csv(PATH)
        df.to_csv('expenses.csv', index=None)