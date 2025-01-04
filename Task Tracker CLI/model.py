from datetime import datetime
import json

FILE_PATH = "database.json"

def get_id():
    with open(FILE_PATH, 'r') as f:
        data = json.load(f)
    
    if len(data) == 0:
        return 1
    
    else:
        return data[-1]['id'] + 1

class Task:
    def __init__(self, description):
        self.id = get_id()
        self.description = description
        self.status = 'todo'
        self.createdAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.updatedAt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    