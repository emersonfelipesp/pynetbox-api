from fastapi import FastAPI, Query, Path, Depends, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import List, Annotated, Any
from contextlib import asynccontextmanager
#from pynetbox_api import nb
from pynetbox_api.exceptions import FastAPIException
from pynetbox_api.api.routes import netbox_router

from pynetbox_api.cache import global_cache

# Database Imports
from pynetbox_api.database import SessionDep, NetBoxEndpoint
from sqlmodel import select

@asynccontextmanager
async def lifespan(app: FastAPI):
    from pynetbox_api.database import create_db_and_tables
    create_db_and_tables()
    yield
    
app = FastAPI(
    title='pynetbox API',
    description='FastAPI wrapper for pynetbox',
    version='0.1',
    lifespan=lifespan
)

# Template and Static Files
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

print('app')
app.include_router(netbox_router)

@app.exception_handler(FastAPIException)
async def fastapi_exception_handler(request, exc):
    content: dict = {}
    if exc.message:
        content['message'] = exc.message
    if exc.detail:
        content['detail'] = exc.detail
    if exc.python_exception:
        content['python_exception'] = exc.python_exception
    

    return JSONResponse(
        status_code=exc.status_code,
        content=content
    )

@app.get('/', response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='home.html'
    )

'''
@app.get('/version')
async def get_version():
    return {'version': nb.version}
'''

print('get cache')

@app.get('/cache')
async def get_cache(
    args: Annotated[str, Query(
        title='Cache Key(s) - Development Use Only',
        description='Cache key to retrieve. Use dot notation for nested keys.',
        example='dcim.manufacturers.1'
    )] = None
):
    if not args:
        return global_cache.return_cache()
    else:
        return global_cache.get(args)

print('set cache')

@app.post('/cache')
async def set_cache(
    key: str = Query(
        ...,
        title='Cache Key',
        description='Cache key to set. Use dot notation for nested keys.',
        example='dcim.manufacturers.1'
    ),
    value: Annotated[Any, Query(
        ...,
        title='Cache Value',
        description='Cache value to set',
        example='{"name": "Test"}'
    )] = None
):
    return global_cache.set(key=key, value=value, return_value=True)

#
# Endpoints: /netbox/<endpoint>
#

@app.post('/endpoint')
def create_netbox_endpoint(netbox: NetBoxEndpoint, session: SessionDep) -> NetBoxEndpoint:
    session.add(netbox)
    session.commit()
    session.refresh(netbox)
    return netbox

@app.get('/endpoint')
def get_netbox_endpoints(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
) -> list[NetBoxEndpoint]:
    netbox_endpoints = session.exec(select(NetBoxEndpoint).offset(offset).limit(limit)).all()
    return netbox_endpoints

GetNetBoxEndpoint = Annotated[list[NetBoxEndpoint], Depends(get_netbox_endpoints)]

@app.get('/endpoint/{netbox_id}')
def get_netbox_endpoint(netbox_id: int, session: SessionDep) -> NetBoxEndpoint:
    netbox_endpoint = session.get(NetBoxEndpoint, netbox_id)
    if not netbox_endpoint:
        raise FastAPIException(status_code=404, detail="Netbox Endpoint not found")
    return netbox_endpoint

@app.delete('/endpoint/{netbox_id}')
def delete_netbox_endpoint(netbox_id: int, session: SessionDep) -> dict:
    netbox_endpoint = session.get(NetBoxEndpoint, netbox_id)
    if not netbox_endpoint:
        raise FastAPIException(status_code=404, detail='NetBox Endpoint not found.')
    session.delete(netbox_endpoint)
    session.commit()
    return {'message': 'NetBox Endpoint deleted.'}