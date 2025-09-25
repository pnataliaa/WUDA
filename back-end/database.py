from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from os import environ


load_dotenv()
DB = environ['POSTGRES_DB']
DATABASE_USER = environ['POSTGRES_USER']
DATABASE_PWD = environ['POSTGRES_PASSWORD']
DATABASE_PORT = environ.get("PORT", 5432)
DATABASE_HOST = environ.get("POSTGRES_HOST", "localhost")
DATABASE_URL = f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PWD}@{DATABASE_HOST}:{DATABASE_PORT}/{DB}"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
def init_db():
    import models
    print("Twórz bazę")
  # importujemy modele, żeby Base je zarejestrowało
    models.Base.metadata.create_all(bind=engine)
