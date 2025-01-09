from fastapi import FastAPI, Request, Form
from user import user_route
from admin import admin_route
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

templates = Jinja2Templates('templates')

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key='idk')

app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")


app.include_router(user_route)
app.include_router(admin_route)

@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/login')
async def login_page(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@app.post('/login')
async def authenticate(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == 'john doe' and password == 'password':
        request.session['user'] = 'admin'
        return RedirectResponse(url='/admin', status_code=303)
    return RedirectResponse(url='/not-admin', status_code=303)

@app.get('/not-admin')
async def not_admin(request: Request):
    return templates.TemplateResponse('notAdmin.html', {'request': request})

@app.get('/logout')
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url='/', status_code=303)

@app.get('/calendar')
async def calendar(request: Request):
    return templates.TemplateResponse('calendar.html', {'request': request})