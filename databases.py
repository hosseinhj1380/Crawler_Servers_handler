from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os 
load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
# engine = create_engine('')
engine = create_engine('postgresql://postgres:postgres@localhost:5432/tiktok')
engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# Session = sessionmaker(bind=engine)
# session = Session()
