from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware('http')
async def my_middleware(request: Request, call_next):
    print('request arrived')
    result = await call_next(request)
    print('result = ', result)
