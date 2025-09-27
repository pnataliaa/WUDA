from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from settings import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
def init_db():
    import models
  # importujemy modele, żeby Base je zarejestrowało
    models.Base.metadata.create_all(bind=engine)
