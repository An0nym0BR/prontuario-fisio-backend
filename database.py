from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://clinica_fisio_db_user:aKNW3HfDQlJmi5C1WXDU97qtJ9oOwenw@dpg-d5a3inje5dus73esprg0-a.virginia-postgres.render.com/clinica_fisio_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
