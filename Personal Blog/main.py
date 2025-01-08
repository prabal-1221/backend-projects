from fastapi import FastAPI, Request, Form
from user import user_route
from admin import admin_route
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates('templates')

app = FastAPI()

app.include_router(user_route)
app.include_router(admin_route)

@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/login')
async def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@app.post('/login')
async def authenticate(username: str = Form(...), password: str = Form(...)):
    if username == 'john doe' and password == 'password':
        return RedirectResponse(url='/admin', status_code=303)
    return RedirectResponse(url='/not-admin', status_code=303)

@app.get('/not-admin')
async def not_admin(request: Request):
    return templates.TemplateResponse('notAdmin.html', {'request': request})