import sqlite3
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Session


# UrL should be in this format:
# DATABASE_TYPE://USERNAME:PASSWORD@HOST/DATABASE_NAME
DATABASE_URL = 'sqlite:///./test.db'


engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread': False}
)
# What is engine?
# The Engine is SQLAlchemy's central database object.
# It contains/configures the machinery required to communicate with SQLite.
# SQLAlchemy doesn't directly talk to the operating system/database server itself.
# It uses a Python database driver : DBAPI driver
# 
#                   SQLAlchemy
#                       │
#                     Engine
#                       │
#               ┌───────┴───────┐
#               │               │
#         Connection Pool     Dialect
#               │               │
#           Connections       SQLite


localSession = sessionmaker(bind=engine)
# 'sessionmaker' does not make sessions.
# Instead it creates a Session factory configured to use that Engine.


# DATABASE_URL
#      │
#      │ configuration
#      ▼
#   ENGINE
#      │
#      │ provides connectivity
#      ▼
#  SESSION FACTORY
#      │
#      │ creates
#      ▼
#   SESSION
#      │
#      │ needs DB work
#      ▼
#  CONNECTION
#      │
#      ▼



Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(String)

Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_database():
    db = localSession()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def home(db: Session = Depends(get_database)):
    return {
        'message': 'db connected fine'
    }
