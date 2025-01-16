from fastapi import APIRouter, Depends, HTTPException, status
from .task_model import Task
from .task_vo import TaskRequest
from sqlalchemy.orm import Session
from typing import Annotated

import sys
sys.path.append('..')
from database import init_db

sys.path.append('..')
from users.user_controller import get_current_user

task_route = APIRouter('/todos')

db_dependency = Annotated[Session, init_db]
user_dependency = Annotated[dict, get_current_user]

@task_route.post('/')
def create_task(task_data: TaskRequest, db: db_dependency, user: user_dependency):
    if not user:
        return {'message': 'Unauthorized'}

    new_task = Task(
        title = task_data.title,
        description = task_data.description,
        user_id = user['user_id']
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@task_route.put('/{task_id}')
def update_task(task_id: int, task_data: TaskRequest, db: db_dependency, user: user_dependency):
    if not user:
        return {'message': 'Forbidden'}

    task = db.query(Task).filter(Task.task_id == task_id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not Found.')
    
    task.title = task_data.title
    task.description = task_data.description

    db.commit()
    db.refresh(task)

    return task

@task_route.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: db_dependency, user: user_dependency):
    if not user:
        return {'message': 'Forbidden'}

    task = db.query(Task).filter(Task.task_id == task_id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not Found.')
    
    db.delete(task)
    db.commit()

@task_route.get('/')
def get_tasks(page: int, limit: int, db: db_dependency, user: user_dependency):
    if not user:
        return {'message': 'Forbidden'}
    
    start = (page-1)*limit
    end = start + limit

    tasks = db.query(Task).all()
    total = len(tasks)

    prev = None
    if page != 1:
        prev = f'/todos?page={page-1}&limit={limit}'
    
    next = None
    if page*limit >= total:
        next = f'/todos?page={page+1}&limit={limit}'

    return {'data': tasks[start: end], 'page': page, 'limit': limit, 'total': total, 'prev': prev, 'next': next}