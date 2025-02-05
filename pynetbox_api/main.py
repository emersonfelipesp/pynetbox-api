from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def homepage():
    return {'message': 'Welcome to pynetbox API'}