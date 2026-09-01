from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserData(BaseModel):
    id: int
    name: str
    age: int

# eg. of dynamic path
@app.get('/user/{user_id}')
def get_user(user_id: int):
    return {
        'user_id': user_id,
        'name': 'some_name'
    }

# eg. of query params, here user_data is query parameter
@app.post('/user')
def create_user(user_data: UserData):
    return {
        'message': 'User data created.',
        'error': {},
        'data': user_data
    }

