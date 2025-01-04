import os
from dao import ExpenseDao
import argparse

def main():
    parser = argparse.ArgumentParser(description='A Simple CLI Program.')
    subparsers = parser.add_subparsers(dest='command', help='Available Commands')

    # add
    add_parser = subparsers.add_parser('add', help='Add a new Expense.')
    add_parser.add_argument('--description', type=str, required=True, help='Description of the Expense.')
    add_parser.add_argument('--amount', type=int, required=True, help='Amount of the Expense.')

    # list
    list_parser = subparsers.add_parser('list', help='List all the Expenses.')
    
    # summary
    summary_parser = subparsers.add_parser('summary', help='Summary of all Expenses.')
    summary_parser.add_argument('--month', type=int, required=False, help='Filter by Month')
    
    # delete
    delete_parser = subparsers.add_parser('delete', help='Delete a particular Expense.')
    delete_parser.add_argument('--id', type=int, required=True, help='ID of the Expense to be deleted.')
    
    # add
    update_parser = subparsers.add_parser('update', help='Update a particular Expense.')
    update_parser.add_argument('--id', type=int, required=True, help='ID of the Expense.')
    update_parser.add_argument('--description', type=str, required=True, help='Description of the Expense.')
    update_parser.add_argument('--amount', type=int, required=True, help='Amount of the Expense.')

    # export
    export_parser = subparsers.add_parser('export', help='Export all the Expenses to a CSV file.')


    args = parser.parse_args()

    if args.command == 'add':
        ExpenseDao.add_expense(args.description, args.amount)
    
    if args.command == 'list':
        ExpenseDao.print_expenses()
    
    if args.command == 'summary':
        month = args.month

        if month is None:
            ExpenseDao.summary_expense()
        else:
            ExpenseDao.summary_expense_month(month)
        
    
    if args.command == 'delete':
        ExpenseDao.delete_expense(args.id)
    
    if args.command == 'update':
        ExpenseDao.update_expense(args.id, args.description, args.amount)
    
    if args.command == 'export':
        ExpenseDao.export_expenses()

if __name__ == '__main__':
    if not os.path.exists('database.txt'):
        with open('database.txt', 'w+') as f:
            f.write('id,date,description,amount\n')
    main()
