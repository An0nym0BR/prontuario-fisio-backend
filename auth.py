from passlib.context import CryptContext
from jose import jwt

SECRET_KEY = "MUDE_ISSO_EM_PRODUCAO"
pwd_context = CryptContext(schemes=["bcrypt"])

def hash_senha(senha):
    return pwd_context.hash(senha)

def verificar_senha(senha, hash):
    return pwd_context.verify(senha, hash)

def criar_token(dados):
    return jwt.encode(dados, SECRET_KEY, algorithm="HS256")
