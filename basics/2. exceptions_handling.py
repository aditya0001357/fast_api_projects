from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class UserDetails(BaseModel):
    id: int
    name: str
    age: int

user_details = {
    1: UserDetails(id=1, name='adam', age=26),
    2: UserDetails(id=2, name='shazam', age=14),
    3: UserDetails(id=3, name='clark', age=28)
}

@app.get('/user/{user_id}')
def get_user(user_id: int):
    if user_id not in user_details:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )
    
    print(f'\nuser_details = {user_details[user_id]}, user_id = {user_id}')
    print(user_details[user_id])
    return {
        'id': user_details[user_id].id,
        'name': user_details[user_id].name,
        'age': user_details[user_id].age,
    }


class UserNotFoundException(Exception):
    def __init__(self, e):
        self.exc = e

@app.exception_handler(UserNotFoundException)
def user_not_found(request: Request, e: UserNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            'status': 'Error',
            'message': f'User {e.exc} not found',
        }
    )
