from fastapi import FastAPI
from typing import Callable
from enum import Enum
from fastapi.responses import JSONResponse

class HTTPMethod(Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"

def create_endpoints(
    app: Callable,
    class_instance
):
    async def get_all():
        return class_instance().all()

    async def get(id: int):
        return class_instance().get(id=id)

    async def placeholder():
        return class_instance(bootstrap_placeholder=True).result

    async def post(data: class_instance.schema_in):
        return class_instance(**data.model_dump(exclude_unset=True))

    async def put(id: int, data: class_instance.schema_in):
        return class_instance().update(id=id, json=data.model_dump(exclude_unset=True))

    async def delete(id: int) -> JSONResponse:
        return class_instance().delete(id=id)

    handlers = {
        'get_all': get_all,
        'get': get,
        'placeholder': placeholder,
        'post': post,
        'put': put,
        'delete': delete
    }

    app.get('/', response_model=class_instance.schema_list)(handlers['get_all'])
    app.get('/{id}', response_model=class_instance.schema)(handlers['get'])
    app.get('/placeholder', response_model=class_instance.schema)(handlers['placeholder'])
    app.post('/', response_model=class_instance.schema)(handlers['post'])
    app.put('/{id}')(handlers['put'])
    app.delete('/{id}')(handlers['delete'])