from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext

app = FastAPI()


ALGORITHM = 'SHA256'
SECRET_KEY = 'mysecret'
ACCESS_TOKEN_EXPIRY_MINUTES = 30


# password hashing
pwd_context = CryptContext(schemes=['bycrypt'], deprecated='auto')
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(raw_password, hashed_password):
    return pwd_context.verify(raw_password, hashed_password)


# dummy user db
fake_user_db = {
    'admin': {
        'username': 'admin',
        'password': pwd_context.hash('1234')
    }
}

# oauth setup
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({
        'exp': expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token



def verify_token(token: str = Header(None)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise HTTPException(
                status_code=401,
                detail='Invalid token'
            )
        return username
    except JWTError :
        raise HTTPException(
            status_code=401,
            detail='Invalid or expred token'
        )


@app.get('/protected')
def protected_route(username: str = Depends(verify_token)):
    return {
        'message': 'You have access to this protected route.',
        'username': username
    }
