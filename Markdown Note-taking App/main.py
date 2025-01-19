from fastapi import FastAPI, UploadFile, File, status, Response
import os
import language_tool_python
from vo import NoteRequest
import markdown

tool = language_tool_python.LanguageTool('en')

NOTES = './notes'
os.makedirs(NOTES, exist_ok=True)

app = FastAPI()

@app.post('/check-grammar')
def check_grammar(note_data: NoteRequest):
    matches = tool.check(note_data.content)

    data = []

    for match in matches:
        data.append({'message': match.message, 'suggestion': match.replacements})

    return data

@app.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_text_file(file_upload: UploadFile = File(...)):

    files = []
    for _, _, file in os.walk(NOTES):
        files.append(file)

    if len(files) == 0:
        filename = '1.md'
    else:
        last_file = files[0][-1]
        filename = str(int(last_file.split('.')[0]) + 1) + '.md'

    text_content = ""
    while chunk := await file_upload.read(1024):
        text_content += chunk.decode("utf-8")

    with open(NOTES + '/' + filename, 'w') as f:
        f.write(text_content)

@app.get('/notes')
def get_all_notes():
    files = []

    for _, _, file in os.walk(NOTES):
        files.append(file)
    
    return {'notes': files}

@app.get('/notes/{note_id}')
def get_note(note_id: str):
    filename = note_id + '.md'

    with open(NOTES + '/' + filename, 'r') as f:
        content = f.read()
    
    markdown_content = markdown.markdown(content)

    return Response(content=markdown_content, media_type='text/html')