import sys
import os
from dao import TaskDao

FILE_PATH = "database.json"

def main():
    arguments = sys.argv
    arguments = arguments[1:] # as first will be file name

    if arguments[0] == 'add':
        TaskDao.add_task(arguments[1])
      
    if arguments[0] == 'delete':
        TaskDao.delete_task(arguments[1])
    
    if arguments[0] == 'mark-in-progress' or arguments[0] == 'mark-done':
        TaskDao.change_status(arguments[1], arguments[0][5:])
    
    if arguments[0] == 'update':
        TaskDao.update_task(arguments[1], arguments[2])

    if arguments[0] == 'list':
        if len(arguments) == 1:
            TaskDao.list_all_tasks()
        
        else:
            TaskDao.filter_tasks(arguments[1])
        
if __name__ == "__main__":

    # to create file it doesn't exist
    if not os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'w') as f:
            f.write('[]')

    main()