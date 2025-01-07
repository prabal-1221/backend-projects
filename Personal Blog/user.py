from fastapi import APIRouter, Request
from os import walk
import json
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates('templates')

user_route = APIRouter()

@user_route.get('/home')
async def articles_list(request: Request):
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

    return templates.TemplateResponse('index.html', {'request': request, 'articles':articles})

@user_route.get('/article/{article_id}')
async def one_article(article_id: int, request: Request):
    with open('articles/'+f'{article_id}.json', 'r') as f:
        article = json.load(f)
    
    return templates.TemplateResponse('article.html', {'request': request, 'article': article})
    