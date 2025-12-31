from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Prontuário Fisioterapia")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MODELO DE DADOS
class Login(BaseModel):
    email: str
    senha: str

# USUÁRIO FIXO (TESTE)
USUARIO_TESTE = {
    "email": "admin@clinica.com",
    "senha": "123"
}

@app.post("/login")
def login(dados: Login):
    if dados.email == USUARIO_TESTE["email"] and dados.senha == USUARIO_TESTE["senha"]:
        return {"token": "token_exemplo"}
    raise HTTPException(status_code=401, detail="Login inválido")