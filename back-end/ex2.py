from fastapi import FastAPI, Request, Depends, HTTPException, status, Cookie, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated

class Usuario(BaseModel):
    nome: str
    idade: float
    bio: str

app = FastAPI()

usuarios = []
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request:Request):
    return templates.TemplateResponse(
        request=request, name="cadastro.html", context={}
    )   



@app.get("/login")
async def get_cadastro_page(request:Request):
    return templates.TemplateResponse(
        request=request, name="login.html", context={}
    )

@app.post("/users")
async def sing_up_users(usuario :Usuario,response: Response):
    usuarios.append(usuario)
    response.set_cookie(key="session_user",value = Usuario.nome)
    return {
        "mensagem": f"Usuário {usuario.nome} criado",
            "dados_recebidos": usuario
    }

# 2. A Dependência: Lendo o Cookie
def get_active_user(session_user: Annotated[str | None, Cookie()] = None):
    # O FastAPI busca automaticamente um cookie chamado 'session_user'
    if not session_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acesso negado: você não está logado."
        )    
    user = next((usuario for usuario in usuarios if usuario.nome == session_user), None)
    if not user:
        raise HTTPException(status_code=401, detail="Sessão inválida")
    
    return user


@app.get("/home")
def show_profile(request: Request, user: dict = Depends(get_active_user)):
    return templates.TemplateResponse(
        request=request, 
        name="profile.html", 
        context={"nome": user.nome,"bio": user.bio}
    )
 