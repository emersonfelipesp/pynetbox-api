from fastapi import FastAPI
from fastapi.responses import JSONResponse

from pynetbox_api import nb
from pynetbox_api.exceptions import FastAPIException
from pynetbox_api.api.routes import netbox_router

app = FastAPI()
app.include_router(netbox_router)

@app.exception_handler(FastAPIException)
async def fastapi_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            'error': exc.message,
            'python_exception': exc.python_exception
        })

@app.get('/')
async def homepage():
    return {'message': 'Welcome to pynetbox API'}

@app.get('/version')
async def get_version():
    return {'version': nb.version}