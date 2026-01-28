# [Task]: T-003
# [From]: specs/constitution.md

import os
from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    # Only run this if you want to create tables locally. 
    # For Neon, usually handled via migrations or direct apply.
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
