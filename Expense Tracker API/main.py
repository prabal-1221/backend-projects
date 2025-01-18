from fastapi import FastAPI
from user.user_controller import user_route
from expense.expense_controller import expense_route
from database import create_db

create_db()

app = FastAPI()
app.include_router(user_route)
app.include_router(expense_route)


@app.get('/')
def index():
    return {'message': 'server is running.'}