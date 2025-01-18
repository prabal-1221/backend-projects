from fastapi import APIRouter, Depends, HTTPException, status
import sys
sys.path.append('..')
from user.user_controller import get_current_user
from typing import Annotated, Optional
from .expense_vo import ExpenseRequest
from .expense_model import Expense
from sqlalchemy.orm import Session
from datetime import date, timedelta

import sys
sys.path.append('..')
from database import init_db

expense_route = APIRouter(prefix='/expense')

user_dependency = Annotated[dict, Depends(get_current_user)]
db_dependecy = Annotated[Session, Depends(init_db)]

@expense_route.post('/')
def create_expense(expense_data: ExpenseRequest, user: user_dependency, db: db_dependecy):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not autheticated.')
    
    new_expense = Expense(
        category = expense_data.category,
        description = expense_data.description,
        amount = expense_data.amount,
        date = expense_data.date,
        user_id = user['user_id']
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense

@expense_route.delete('/{expense_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, user: user_dependency, db: db_dependecy):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not autheticated.')

    expense = db.query(Expense).filter(Expense.expense_id == expense_id).first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='expense not found.')
    
    db.delete(expense)
    db.commit()

@expense_route.put('/{expense_id}')
def update_expense(expense_id: int, expense_data: ExpenseRequest, user: user_dependency, db: db_dependecy):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not autheticated.')
    
    expense = db.query(Expense).filter(Expense.expense_id == expense_id).first()

    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='expense not found.')
    
    expense.category = expense_data.category if expense_data.category is not None else expense.category
    expense.description = expense_data.description if expense_data.description is not None else expense.description
    expense.amount = expense_data.amount if expense_data.amount is not None else expense.amount
    expense.date = expense_data.date if expense_data.date is not None else expense.date

    db.commit()

    return expense

@expense_route.get('/week')
def get_expenses_week(user: user_dependency, db: db_dependecy):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not autheticated.')

    today = date.today()
    start_date = today - timedelta(days=today.weekday())

    expenses = filter_expense(start_date, None, db)

    return expenses

@expense_route.get('/month')
def get_expenses_month(user: user_dependency, db: db_dependecy):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not autheticated.')

    today = date.today()
    start_date = today.replace(day=1)

    expenses = filter_expense(start_date, None, db)

    return expenses

@expense_route.get('/three_month')
def get_expenses_three_month(user: user_dependency, db: db_dependecy):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not autheticated.')
    
    today = date.today()
    start_current_month = today.replace(day=1)
    start_date = start_current_month - timedelta(days=90)

    expenses = filter_expense(start_date, None, db)

    return expenses

@expense_route.get('/')
def get_expenses_by_date(user: user_dependency, db: db_dependecy, start_date: Optional[date] = None, end_date: Optional[date] = None):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not autheticated.')
    
    if (not start_date) and (not end_date):
        return db.query(Expense).all()
    
    elif ((not start_date) and end_date) or ((not end_date) and start_date):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='provide both dates for filtering.')

    expenses = filter_expense(start_date, end_date, db)

    return expenses

def filter_expense(start_date, end_date, db: Session):

    if not end_date:
        filtered_expenses = db.query(Expense).filter(
            Expense.date >= start_date
        ).all()

        return filtered_expenses

    filtered_expenses = db.query(Expense).filter(
        Expense.date >= start_date,
        Expense.date <= end_date
    ).all()

    return filtered_expenses