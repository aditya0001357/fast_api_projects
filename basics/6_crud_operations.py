import sqlite3
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, Session


DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine( 
    DATABASE_URL,
    connect_args={'check_same_thread': False}
)
localSession = sessionmaker(bind=engine)


Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(String)

Base.metadata.create_all(bind=engine)

def get_database():
    db = localSession()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

@app.post('/todos')
def create_todo(title: str, db: Session = Depends(get_database)):
    todo = Todo(title, complete='False')
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {
        'message': 'todo created',
        'data': todo
    }
    
