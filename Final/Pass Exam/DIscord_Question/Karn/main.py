from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

app = FastAPI()

data = { 1: {"title" : "Shitting on the floor."},
         2: {"title" : "Peeing in the sink."}}

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("to_do_list.html", {"request": request, "data": data})

@app.get("/list/{item_id}", response_class=HTMLResponse)
async def read_item(item_id: int, request: Request):
    item = data.get(item_id)
    return templates.TemplateResponse("item.html", {"request": request, "item": item})