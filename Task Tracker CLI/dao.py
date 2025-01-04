import json
from model import Task
from datetime import datetime

FILE_PATH = "database.json"

def json_read():
    with open(FILE_PATH, 'r') as f:
        file_data = json.load(f)
    
    return file_data

def json_write_one_task(data):
    with open(FILE_PATH, 'r') as f:
        file_data = json.load(f)
    
    if str(type(data)) != "<class 'dict'>":
        file_data.append(data.__dict__)
    else:
        file_data.append(data)

    with open(FILE_PATH, 'w') as f:
        json.dump(file_data, f, indent=4)

def json_write(data):
    with open(FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

class TaskDao:
    def add_task(description):
        new_task = Task(description=description)
        json_write_one_task(new_task)
        print(new_task.__dict__)
    
    def update_task(id, description):
        file_data = json_read()
        json_write([])

        for task in file_data:
            if task['id'] == int(id):
                task['description'] = description
                task['updatedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(task)

            json_write_one_task(task)
        
    def delete_task(id):
        file_data = json_read()
        json_write([])

        for task in file_data:
            if task['id'] == int(id):
                print(task)
                continue
            json_write_one_task(task)
            
    
    def change_status(id, status):
        file_data = json_read()
        json_write([])

        for task in file_data:
            if task['id'] == int(id):
                task['status'] = status
                task['updatedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(task)
            json_write_one_task(task)
    
    def list_all_tasks():
        print(json.dumps(json_read(), indent=4))
    
    def filter_tasks(filter):
        file_data = json_read()
        
        filter_tasks = []

        for task in file_data:
            if task['status'] == filter:
                filter_tasks.append(task)
        
        print(json.dumps(filter_tasks, indent=4))
