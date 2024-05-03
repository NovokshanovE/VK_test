from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
PORT = os.getenv("DATABASE_PORT")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
USER = os.getenv("POSTGRES_USER")
DB = os.getenv("POSTGRES_DB")
HOST = os.getenv("POSTGRES_HOST")
HOSTNAME = os.getenv("POSTGRES_HOSTNAME")
SECRET_KEY = os.getenv("SECRET_KEY")
DB_URL = f"{HOST}://{USER}:{PASSWORD}@{HOSTNAME}:{PORT}/{DB}"
print(DB_URL)

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
