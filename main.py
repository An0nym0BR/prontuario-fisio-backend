from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Login(BaseModel):
    email: str
    senha: str
    
@app.get("/")
def root():
    return {"status": "ok"}

USUARIO_TESTE = {
    "email": "admin@clinica.com",
    "senha": "123"
}

@app.post("/login")
def login(dados: Login):
    if dados.email == USUARIO_TESTE["email"] and dados.senha == USUARIO_TESTE["senha"]:
        return {"token": "token_exemplo"}
    raise HTTPException(status_code=401, detail="Login inválido")