from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha_hash = Column(String)
    perfil = Column(String)

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    nascimento = Column(Date)
    sexo = Column(String)
    telefone = Column(String)

class Atendimento(Base):
    __tablename__ = "atendimentos"
    id = Column(Integer, primary_key=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    data = Column(Date)
    diagnostico_clinico = Column(String)
    diagnostico_fisio = Column(String)
    queixa = Column(String)
    eva = Column(Integer)
    plano = Column(String)
    evolucao = Column(String)
