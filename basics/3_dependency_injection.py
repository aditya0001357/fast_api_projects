from fastapi import FastAPI, Depends, Header
from pydantic import BaseModel

app = FastAPI()


def common_logic():
    return {
        'message': 'common_logic_executed'
    }

@app.get('/home')
def home(data):
    pass

def verify_token(token: str = Header(None)):
    if token == 'correct_token':
        return {
            'user': 'Auth Granted'
        }
    else:
        return {
            'message': 'Access not granted'
        }

@app.get('/secure')
def secure_data(user = Depends(verify_token)):
    return {
        'message': 'Secure data accessed.',
        'user': user
    }
