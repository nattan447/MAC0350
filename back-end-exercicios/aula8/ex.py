from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

estado = {"curtidas": 0}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(name="index.html",request=request ,  context={"request": request})

@app.get("/tab/curtidas", response_class=HTMLResponse)
async def get_curtidas(request: Request):
    return templates.TemplateResponse(name="curtidas.html", request=request,context={"request": request, "curtidas": estado["curtidas"]})

@app.post("/curtir", response_class=HTMLResponse)
async def post_curtir(request: Request, reset: bool = False):
    if reset:
        estado["curtidas"] = 0
    else:
        estado["curtidas"] += 1
    return templates.TemplateResponse(name="curtidas.html", request=request,context={"request": request, "curtidas": estado["curtidas"]})

@app.get("/tab/jupiter", response_class=HTMLResponse)
async def get_jupiter(request: Request):
    return templates.TemplateResponse(name="jupiter.html",request=request ,context={"request": request})

@app.get("/tab/professor", response_class=HTMLResponse)
async def get_professor(request: Request):
    return templates.TemplateResponse(name="professor.html", request=request,context={"request": request})