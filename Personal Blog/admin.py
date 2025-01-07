from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from os import walk
import json

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
        with open('articles/'+file, 'r') as f:
            data = json.load(f)
        file_data.append(data)
    
    for data in file_data:
        articles.append((data['title'], data['date']))

    return templates.TemplateResponse('admin.html', {'request': request, 'articles': articles})