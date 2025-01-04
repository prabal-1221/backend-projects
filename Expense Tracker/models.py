import datetime

PATH = 'database.txt'

def read_expense():
    with open(PATH, 'r') as f:
        last_line = ''
        for line in f.readlines():
            last_line = line
    
    id, _, _, _ = last_line.split(',')
    if id == 'id':
        return 1
    else:
        return int(id)+1

class Expense:
    def __init__(self, description, amount):
        self.id = read_expense()
        self.description = description
        self.amount = amount
        self.createdAt = datetime.datetime.now().strftime('%Y-%m-%d')
    
    def __repr__(self):
        return f'{self.id},{self.createdAt},{self.description},{self.amount}'
    
    def __str__(self):
        return f'{self.id},{self.createdAt},{self.description},{self.amount}'