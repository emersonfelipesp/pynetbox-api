from pydantic import BaseModel

class ValueLabelSchema(BaseModel):
    value: str | None = None
    label: str | None = None

class StatusSchema(BaseModel):
    value: str | None = None
    label: str | None = None