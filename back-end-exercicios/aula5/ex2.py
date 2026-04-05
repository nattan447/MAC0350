from fastapi import FastAPI, Request, Depends, HTTPException, status, Cookie, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated

class Usuario(BaseModel):
    nome: str
    senha: str
    bio: str

class LoginDados(BaseModel):
    nome: str
    senha: str

app = FastAPI()

usuarios = []
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        name="cadastro.html",request=request,context= {"request": request}
    )

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse(
       name= "login.html",request=request,context= {"request": request}
    )

@app.post("/users")
async def sign_up_users(usuario: Usuario):
    usuarios.append(usuario)
    return {"mensagem": f"Usuário {usuario.nome} criado com sucesso"}

@app.post("/login")
async def login(dados: LoginDados, response: Response):
    user = next((u for u in usuarios if u.nome == dados.nome and u.senha == dados.senha), None)
    
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")
    
    response.set_cookie(key="session_user", value=user.nome)
    return {"mensagem": "Login realizado"}

def get_active_user(session_user: Annotated[str | None, Cookie()] = None):
    if not session_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não logado"
        )
    
    user = next((u for u in usuarios if u.nome == session_user), None)
    if not user:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    
    return user

@app.get("/home")
def show_profile(request: Request, user: Usuario = Depends(get_active_user)):
    return templates.TemplateResponse(
       name= "profile.html", 
        request=request,context={"request": request, "nome": user.nome, "bio": user.bio}
    )