from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

data = {
    "notes": {
        1 : {
            "title": "Note 1",
            "body": "This is a note 1"
        },
        2 : {
            "title": "Note 2",
            "body": "This is a note 2"
        },
    },
}

@app.get("/home", response_class=HTMLResponse)
async def login_page(request: Request):    
    return templates.TemplateResponse("index.html", {"request": request, "data": data})

@app.get("/notes/{note_id}", response_class=HTMLResponse)
async def read_notes(note_id: int, request: Request):
    note = data["notes"].get(note_id)
    return templates.TemplateResponse("notes.html", {"request": request, "note": note})

@app.get("/create-note", response_class=HTMLResponse)
async def create_note_page(request: Request):
    return templates.TemplateResponse("create_note.html", {"request": request})

@app.post("/create", response_class=RedirectResponse)
async def create_note(title: str = Form(...), body: str = Form(...)):
    note_id = len(data["notes"]) + 1
    data["notes"][note_id] = {
        "title": title,
        "body": body
    }
    return RedirectResponse(f"/notes/{note_id}", status_code=302)