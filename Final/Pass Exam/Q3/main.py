from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

data = {
    1: {"title": "Note 1", "content": "Content of Note 1"},
    2: {"title": "Note 2", "content": "Content of Note 2"}
}

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def list_notes(request: Request):
    return templates.TemplateResponse("note_list.html", {"request": request, "data": data})

@app.get("/note/{note_id}", response_class=HTMLResponse)
async def get_note_detail(note_id: int, request: Request):
    data_1 = data.get(note_id)
    return templates.TemplateResponse("note_details.html", {"request": request, "data": data_1})

@app.get("/note/{note_id}/edit", response_class=HTMLResponse)
async def edit_note(note_id: int, request: Request):
    data_1 = data.get(note_id)
    return templates.TemplateResponse("note_edit.html", {"request": request, "note_id": note_id, "data": data_1})
