from fastapi import APIRouter, Request,Form
from fastapi.templating import Jinja2Templates
from os import walk
import json
from fastapi.responses import RedirectResponse
import os
import json
from main import LOG_IN

templates = Jinja2Templates('templates')

admin_route = APIRouter()

@admin_route.get('/admin')
async def article_list(request: Request):
    articles = []

    files = []
    for _,_,filenames in walk('articles'):
        files.extend(filenames)

    file_data = []
    for file in filenames:
        filename = file.split('.')[0]
        with open('articles/'+file, 'r') as f:
            data = json.load(f)
        file_data.append((data, filename))
    
    for data in file_data:
        articles.append((data[0]['title'], data[0]['date'], data[1]))

    return templates.TemplateResponse('admin.html', {'request': request, 'articles':articles})

@admin_route.get('/add')
async def add_article(request: Request):
    return templates.TemplateResponse('add.html', {'request': request})

@admin_route.post("/add")
async def add_article(title: str = Form(...), date: str = Form(...), content: str = Form(...)):

    files = os.listdir('articles')
    filename = str(int(files[-1].split('.')[0])+1) + '.json'

    data = {'title': title, 'date': date, 'content': content}

    with open('articles/'+filename, 'w') as f:
        json.dump(data, f, indent=4)

    return RedirectResponse(url="/admin", status_code=303)

@admin_route.get('/update/{article_id}')
async def add_article(article_id: str, request: Request):
    with open('articles/'+f'{article_id}.json', 'r') as f:
        article = json.load(f)
    return templates.TemplateResponse('update.html', {'request': request, 'article': article, 'article_id': article_id})

@admin_route.post("/update/{article_id}")
async def add_article(article_id: str, title: str = Form(...), date: str = Form(...), content: str = Form(...)):

    data = {'title': title, 'date': date, 'content': content}

    with open('articles/'+article_id+'.json', 'w') as f:
        json.dump(data, f, indent=4)

    return RedirectResponse(url="/admin", status_code=303)

@admin_route.get("/delete/{article_id}")
async def add_article(article_id: str):
    os.remove('articles/'+article_id+'.json')

    return RedirectResponse(url="/admin", status_code=303)