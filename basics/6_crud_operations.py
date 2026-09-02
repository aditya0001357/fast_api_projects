from fastapi import FastAPI, Depends, HTTPException
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
    todo = Todo(title=title, completed='False')
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {
        'message': 'todo created',
        'data': todo
    }


@app.get('/todos')
def get_all_todos(db: Session = Depends(get_database)):
    all_todos = db.query(Todo).all()
    return {
        'message': f'These are all the {len(all_todos)} todos available so far.',
        'data': all_todos
    }


@app.get('/todos/{todo_id}')
def get_todo(todo_id: int, db: Session = Depends(get_database)):
    
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).one()
    except:
        raise HTTPException(status_code=404, detail='Todo not found.')

    return todo


@app.put('/todos/{todo_id}')
def update_todo(todo_id: int, title: str, db: Session = Depends(get_database)):
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).one()
    except:
        raise HTTPException(status_code=404, detail='Todo not found.') 

    todo.title = title

    db.commit(); db.refresh(todo)
    return {
        'message': 'Updated the target todo.',
        'data': todo
    }   


@app.delete('/todos/{todo_id}')
def delete_todo(todo_id: int, db: Session = Depends(get_database)):
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).one()
    except:
        raise HTTPException(status_code=404, detail='Todo not found.') 

    db.delete(todo)
    db.commit()
    return {
        'message': 'Deleted the target todo.',
        'data': todo
    }
