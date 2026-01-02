import os
from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


# ========================
# MODELOS PYDANTIC
# ========================

class PacienteCreate(BaseModel):
   nome: str
    cpf: str
    telefone: str
    diagnostico: Optional[str] = None
    sexo: Optional[str] = None
    data_nascimento: Optional[date] = None
    queixa_principal: Optional[str] = None
    historico_clinico: Optional[str] = None
    medicacoes: Optional[str] = None
    observacoes: Optional[str] = None

class PacienteResponse(BaseModel):
    id: int
    nome: str
    cpf: str
    telefone: str
    diagnostico: Optional[str] = None

class Config:
        from_attributes = True
        

class Paciente(BaseModel):
    nome: str
    cpf: str
    telefone: str
    diagnostico: Optional[str] = None
    sexo: Optional[str] = None
    data_nascimento: Optional[date] = None
    queixa_principal: Optional[str] = None
    historico_clinico: Optional[str] = None
    medicacoes: Optional[str] = None
    observacoes: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    senha: str


class Profissional(BaseModel):
    nome: str
    email: str
    senha: str
    

# ========================
# APP
# ========================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================
# BANCO DE DADOS
# ========================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não definida")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()


# ========================
# MODELOS DO BANCO
# ========================

class PacienteDB(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    cpf = Column(String)
    telefone = Column(String)
    idade = Column(Integer)
    sexo = Column(String)
    data_nascimento = Column(String)
    diagnostico = Column(String)
    queixa_principal = Column(String)
    historico_clinico = Column(String)
    medicacoes = Column(String)
    observacoes = Column(String)


class ProfissionalDB(Base):
    __tablename__ = "profissionais"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha = Column(String)

# ========================
# CRIAR TABELAS
# ========================

Base.metadata.create_all(bind=engine)

# ========================
# ROTAS
# ========================

@app.post("/profissionais")
def criar_profissional(prof: Profissional):
    db = SessionLocal()

    total = db.query(ProfissionalDB).count()
    if total >= 5:
        db.close()
        raise HTTPException(status_code=400, detail="Limite de profissionais atingido")

    existe = db.query(ProfissionalDB).filter(
        ProfissionalDB.email == prof.email
    ).first()
    if existe:
        db.close()
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    novo = ProfissionalDB(
        nome=prof.nome,
        email=prof.email,
        senha=prof.senha
    )
    db.add(novo)
    db.commit()
    db.close()

    return {"mensagem": "Profissional cadastrado com sucesso"}


@app.post("/login")
def login(dados: LoginRequest):
    db = SessionLocal()
    user = db.query(ProfissionalDB).filter(
        ProfissionalDB.email == dados.email,
        ProfissionalDB.senha == dados.senha
    ).first()
    db.close()

    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return {
        "mensagem": "Login realizado com sucesso",
        "usuario": {
            "id": user.id,
            "nome": user.nome,
            "email": user.email
        }
    }

################
# CRIAR PACIENTE
################
@app.post("/pacientes")
def criar_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    novo = Paciente(**paciente.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

##################
# LISTAR PACIENTES
##################
@app.get("/pacientes")
def listar_pacientes(db: Session = Depends(get_db)):
    return db.query(Paciente).all()
