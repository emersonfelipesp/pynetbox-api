from pydantic import BaseModel

class StatusSchema(BaseModel):
    value: str | None = None
    label: str | None = None