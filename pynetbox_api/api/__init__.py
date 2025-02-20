from fastapi import FastAPI
from typing import Callable
from enum import Enum
from fastapi.responses import JSONResponse

def create_endpoints(
    class_instance
):
    """
    Class-Based Route Generator
    """
    async def get_all():
        return class_instance().all()

    async def get(id: int):
        return class_instance().get(id=id)

    async def placeholder():
        return class_instance(
            bootstrap_placeholder=True,
            is_bootstrap=True,
            cache=True
        ).result

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

    class_instance.api_router.get('/', response_model=class_instance.schema_list)(handlers['get_all'])
    class_instance.api_router.get('/{id}', response_model=class_instance.schema)(handlers['get'])
    class_instance.api_router.get('/placeholder/', response_model=class_instance.schema)(handlers['placeholder'])
    class_instance.api_router.post('/', response_model=class_instance.schema)(handlers['post'])
    class_instance.api_router.put('/{id}')(handlers['put'])
    class_instance.api_router.delete('/{id}')(handlers['delete'])