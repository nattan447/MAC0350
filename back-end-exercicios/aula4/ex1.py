from fastapi import FastAPI, Request 
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request:Request):
    return templates.TemplateResponse(
        request=request, name="pagina.html", context={}
    )   


class Usuario(BaseModel):
    nome: str
    idade: float
    


listUsers = []
@app.post("/users")
def add_user(usuario: Usuario):
    listUsers.append(usuario)
    return {
        "mensagem": f" Usuário {usuario.nome} adicionado!",
        "total_usuarios": len(listUsers),
        "ultimo_adicionado": usuario
    }


@app.get("/users")
def get_users(indice:int= None):
    if(indice!=None):
        return listUsers[indice]
    return listUsers
@app.delete("/users")
def delete_users():
    print("apagou tudo")
    listUsers.clear()