from fastapi import FastAPI
from pynetbox_api import nb

app = FastAPI()

@app.get('/')
async def homepage():
    return {'message': 'Welcome to pynetbox API'}

@app.get('/version')
async def get_version():
    return {'version': nb.version}